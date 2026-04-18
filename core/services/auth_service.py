from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from google.auth.transport import requests
from google.oauth2 import id_token

from core.schemas.auth import AuthUserResponse, GoogleLoginResponse
from core.settings.google_oauth import GOOGLE_CLIENT_ID, GOOGLE_TOKEN_ISSUERS


class AuthService:
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
        google_user = self.verify_google_token(google_token)
        user = self._get_or_create_user(google_user)
        access_token = self._create_access_token(user)

        return GoogleLoginResponse(
            access_token=access_token,
            user=AuthUserResponse(
                id=user.id,
                email=user.email,
                name=user.get_full_name() or user.email,
                first_name=user.first_name or None,
                last_name=user.last_name or None,
            ),
        )

    def _get_or_create_user(self, google_user: dict):
        User = get_user_model()

        email = google_user["email"].strip().lower()
        full_name = google_user.get("name") or email
        first_name = google_user.get("given_name") or full_name.split(" ", 1)[0]
        last_name = google_user.get("family_name") or ""

        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                "email": email,
                "first_name": first_name[:150],
                "last_name": last_name[:150],
            },
        )

        changed = False
        if user.email != email:
            user.email = email
            changed = True
        if user.first_name != first_name[:150]:
            user.first_name = first_name[:150]
            changed = True
        if user.last_name != last_name[:150]:
            user.last_name = last_name[:150]
            changed = True
        if created:
            user.set_unusable_password()
            changed = True

        if changed:
            user.save()

        return user

    def _create_access_token(self, user) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.get_full_name() or user.email,
            "iat": now,
            "exp": now + timedelta(hours=24),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
