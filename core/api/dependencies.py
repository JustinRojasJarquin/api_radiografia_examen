from __future__ import annotations

from core.settings.security import extract_bearer_token, get_authenticated_user
from core.utils.exceptions import AuthenticationException


def get_bearer_token(request):
    try:
        return extract_bearer_token(request)
    except ValueError as exc:
        raise AuthenticationException(str(exc)) from exc


def require_authenticated_user(request):
    try:
        return get_authenticated_user(request)
    except ValueError as exc:
        raise AuthenticationException(str(exc)) from exc
