from __future__ import annotations

from datetime import datetime, timezone

import jwt
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from core.database.session import SessionLocal
from core.schemas.auth import AuthUserResponse, GoogleLoginResponse
from core.repositories.user_repository import UserRepository
from core.settings.google_oauth import GOOGLE_CLIENT_ID, GOOGLE_TOKEN_ISSUERS
from core.settings.jwt_config import (
    JWT_ACCESS_TOKEN_EXPIRE_DELTA,
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
)


class AuthService:
    def __init__(self, db: Session | None = None):
        self.db = db or SessionLocal()
        self._owns_db = db is None
        self.user_repository = UserRepository()

    def verify_google_token(self, google_token: str) -> dict:
        if not GOOGLE_CLIENT_ID:
            raise ValueError("GOOGLE_CLIENT_ID is not configured")

        try:
            token_info = id_token.verify_oauth2_token(
                google_token,
                requests.Request(),
                GOOGLE_CLIENT_ID,
            )
        except ValueError as exc:
            raise ValueError("Invalid Google token") from exc

        if token_info.get("iss") not in GOOGLE_TOKEN_ISSUERS:
            raise ValueError("Invalid Google token issuer")

        if not token_info.get("email"):
            raise ValueError("Google token does not include an email")

        if token_info.get("email_verified") is False:
            raise ValueError("Google email is not verified")

        return token_info

    def login_with_google(self, google_token: str) -> GoogleLoginResponse:
        try:
            google_user = self.verify_google_token(google_token)
            user = self.get_or_create_user(google_user)
            access_token = self.create_access_token(user)

            return GoogleLoginResponse(
                access_token=access_token,
                user=self._build_auth_user_response(user),
            )
        finally:
            self._close_owned_session()

    def get_or_create_user(self, google_user: dict):
        email = google_user["email"].strip().lower()
        full_name = (google_user.get("name") or email).strip()
        db = self._get_db()

        user, created = self.user_repository.get_or_create(
            db,
            email=email,
            full_name=full_name,
        )

        if not created:
            changes = {}
            if user.full_name != full_name:
                changes["full_name"] = full_name
            if not user.is_active:
                changes["is_active"] = True
            if changes:
                user = self.user_repository.update(db, user, changes)

        return user

    def create_access_token(self, user) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.full_name or user.email,
            "iat": now,
            "exp": now + JWT_ACCESS_TOKEN_EXPIRE_DELTA,
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    def validate_access_token(self, token: str) -> dict:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token payload does not include user id")

        return payload

    def get_authenticated_user(self, token: str):
        try:
            payload = self.validate_access_token(token)
            user_id = int(payload["sub"])
            user = self.user_repository.get_by_id(self._get_db(), user_id)

            if not user or not user.is_active:
                raise ValueError("Authenticated user not found")

            return user
        finally:
            self._close_owned_session()

    def get_authenticated_user_response(self, token: str) -> AuthUserResponse:
        user = self.get_authenticated_user(token)
        return self._build_auth_user_response(user)

    def _build_auth_user_response(self, user) -> AuthUserResponse:
        first_name = user.first_name or None
        last_name = user.last_name or None

        return AuthUserResponse(
            id=user.id,
            email=user.email,
            name=user.full_name or user.email,
            first_name=first_name,
            last_name=last_name,
        )

    def _close_owned_session(self) -> None:
        if self._owns_db and self.db is not None:
            self.db.close()
            self.db = None

    def _get_db(self) -> Session:
        if self.db is None:
            self.db = SessionLocal()
        return self.db
