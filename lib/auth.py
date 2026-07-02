import jwt
import datetime
from typing import Optional
from flask import g, request, jsonify
from config.config import Config

INTERNAL_PREFIXES = ("192.168.1.", "172.", "127.", "192.168.65.")


def is_internal_request() -> bool:
    """
    Returns True if the request originates from a known internal network.
    remote_addr is set by the OS TCP stack and cannot be spoofed by headers.
    Covers: LAN (192.168.1.x), Docker bridge (172.x.x.x), loopback (127.x).
    """
    print("Request remote addr: ", request.remote_addr)
    ip = request.remote_addr
    return any(ip.startswith(prefix) for prefix in INTERNAL_PREFIXES)


def create_token(user_id: int, username: str) -> str:
    payload = {
        "sub": username,
        "user_id": user_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")


def verify_token(token: str) -> dict:
    """
    Decodes and validates the JWT.
    Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError on failure.
    """
    return jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])


def _extract_bearer_token() -> Optional[str]:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header.split(" ", 1)[1]


def check_auth():
    """
    Blueprint before_request hook for general routes.
    - Internal requests (LAN / Docker network) pass through without a token.
    - External requests must include: Authorization: Bearer <token>
    """
    if request.method == "OPTIONS":
        return None

    if is_internal_request():
        return None

    token = _extract_bearer_token()
    if not token:
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    try:
        verify_token(token)
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    return None


def check_user_auth():
    """
    Blueprint before_request hook for user-specific routes.
    Always requires a valid token — no internal bypass.
    Sets g.user_id on success.
    """
    if request.method == "OPTIONS":
        return None

    token = _extract_bearer_token()
    if not token:
        return jsonify({"error": "Authentication required"}), 401

    try:
        payload = verify_token(token)
        g.user_id = payload["user_id"]
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except (jwt.InvalidTokenError, KeyError):
        return jsonify({"error": "Invalid token"}), 401

    return None
