from __future__ import annotations

from django.http import HttpRequest
from jwt import ExpiredSignatureError, InvalidTokenError

from core.services.auth_service import AuthService
from core.settings.jwt_config import JWT_AUTH_HEADER_PREFIX


def extract_bearer_token(request: HttpRequest) -> str:
    auth_header = request.headers.get("Authorization", "").strip()
    prefix = f"{JWT_AUTH_HEADER_PREFIX} "

    if not auth_header or not auth_header.startswith(prefix):
        raise ValueError("Authorization header missing or invalid")

    token = auth_header[len(prefix):].strip()
    if not token:
        raise ValueError("Authorization token is missing")

    return token


def get_authenticated_user(request: HttpRequest):
    token = extract_bearer_token(request)

    try:
        service = AuthService()
        return service.get_authenticated_user(token)
    except ExpiredSignatureError as exc:
        raise ValueError("Token expired") from exc
    except InvalidTokenError as exc:
        raise ValueError("Invalid token") from exc
