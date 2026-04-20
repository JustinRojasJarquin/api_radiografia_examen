from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import jwt
from django.http import HttpRequest
from jwt import ExpiredSignatureError, InvalidTokenError

from core.services.auth_service import AuthService
from core.settings.jwt_config import JWT_AUTH_HEADER_PREFIX


SIGNED_URL_SECRET = os.getenv("SIGNED_URL_SECRET", "change_me_signed_url_secret")
SIGNED_URL_EXPIRE_MINUTES = int(os.getenv("SIGNED_URL_EXPIRE_MINUTES", "5"))
SIGNED_URL_ALGORITHM = "HS256"


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


def create_signed_image_token(user_id: int, record_id: int, image_url: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=SIGNED_URL_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "record_id": record_id,
        "image_url": image_url,
        "type": "signed_image_url",
        "exp": expire,
    }

    return jwt.encode(payload, SIGNED_URL_SECRET, algorithm=SIGNED_URL_ALGORITHM)


def verify_signed_image_token(token: str) -> dict:
    payload = jwt.decode(token, SIGNED_URL_SECRET, algorithms=[SIGNED_URL_ALGORITHM])

    if payload.get("type") != "signed_image_url":
        raise InvalidTokenError("Invalid signed URL token type")

    return payload