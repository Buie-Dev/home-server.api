import jwt
import datetime
from flask import request, jsonify
from config.config import Config

INTERNAL_PREFIXES = ("192.168.1.", "172.", "127.", "192.168.65.")


def is_internal_request() -> bool:
    """
    Returns True if the request originates from a known internal network.
    remote_addr is set by the OS TCP stack and cannot be spoofed by headers.
    Covers: LAN (192.168.1.x), Docker bridge (172.x.x.x), loopback (127.x).
    """
    print("Request ", request)
    print("Request remote addr: ", request.remote_addr)
    ip = request.remote_addr
    return any(ip.startswith(prefix) for prefix in INTERNAL_PREFIXES)


def create_token(username: str) -> str:
    payload = {
        "sub": username,
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


def check_auth():
    """
    Blueprint before_request hook.
    - Internal requests (LAN / Docker network) pass through without a token.
    - External requests must include: Authorization: Bearer <token>
    """
    if is_internal_request():
        return None

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ", 1)[1]
    try:
        verify_token(token)
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    return None
