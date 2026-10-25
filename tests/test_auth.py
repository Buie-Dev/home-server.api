import time
from unittest.mock import patch

import jwt


class TestHealthCheck:
    def test_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.get_json() == {"Status": "Connected"}


class TestCheckAuth:
    def test_internal_ip_bypasses_auth(self, client):
        with patch("lib.auth.is_internal_request", return_value=True):
            response = client.get("/irrigations/zones")
        # Should not get 401 (may get other errors from mocked DB, but not auth failure)
        assert response.status_code != 401

    def test_external_ip_no_token_returns_401(self, client):
        with patch("lib.auth.is_internal_request", return_value=False):
            response = client.get("/irrigations/zones")
        assert response.status_code == 401
        data = response.get_json()
        assert "Missing" in data["error"] or "invalid" in data["error"]

    def test_external_ip_valid_token_passes(self, client, auth_token):
        with patch("lib.auth.is_internal_request", return_value=False):
            response = client.get(
                "/irrigations/zones",
                headers={"Authorization": f"Bearer {auth_token}"},
            )
        assert response.status_code != 401

    def test_external_ip_expired_token_returns_401(self, client):
        token = jwt.encode(
            {"sub": "testuser", "user_id": 1, "iat": time.time() - 7200, "exp": time.time() - 3600},
            "test-secret",
            algorithm="HS256",
        )
        with patch("lib.auth.is_internal_request", return_value=False):
            response = client.get(
                "/irrigations/zones",
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 401
        assert "expired" in response.get_json()["error"].lower()

    def test_external_ip_invalid_token_returns_401(self, client):
        token = jwt.encode(
            {"sub": "testuser", "exp": time.time() + 3600},
            "wrong-secret",
            algorithm="HS256",
        )
        with patch("lib.auth.is_internal_request", return_value=False):
            response = client.get(
                "/irrigations/zones",
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 401
        assert "Invalid" in response.get_json()["error"]

    def test_options_request_bypasses_auth(self, client):
        response = client.options("/irrigations/zones")
        assert response.status_code != 401


class TestCheckUserAuth:
    def test_requires_token_even_for_internal_ip(self, client):
        with patch("lib.auth.is_internal_request", return_value=True):
            response = client.get("/people/")
        assert response.status_code == 401

    def test_valid_token_passes(self, client, auth_token):
        with patch("lib.auth.is_internal_request", return_value=False):
            response = client.get(
                "/people/",
                headers={"Authorization": f"Bearer {auth_token}"},
            )
        assert response.status_code != 401

    def test_options_bypasses_user_auth(self, client):
        response = client.options("/people/")
        assert response.status_code != 401
