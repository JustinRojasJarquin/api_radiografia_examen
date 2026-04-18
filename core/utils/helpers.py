from __future__ import annotations

import json
from typing import Any

from django.http import HttpRequest

from core.utils.exceptions import BadRequestException


def parse_json_body(request: HttpRequest) -> dict[str, Any]:
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError as exc:
        raise BadRequestException("Invalid JSON body") from exc


def get_form_field(request: HttpRequest, name: str, default: Any = None) -> Any:
    return request.POST.get(name, default)


def require_form_field(request: HttpRequest, name: str) -> str:
    value = get_form_field(request, name)
    if value is None or str(value).strip() == "":
        raise BadRequestException(f"Missing required field: {name}")
    return str(value).strip()


def validate_file_type(file, allowed_mime_types: list[str]) -> None:
    content_type = getattr(file, "content_type", "")
    if content_type not in allowed_mime_types:
        raise BadRequestException(f"Invalid file type: {content_type}")


def validate_max_file_size(file, max_size_bytes: int) -> None:
    size = getattr(file, "size", None)
    if size is None:
        raise BadRequestException("Unable to determine file size")

    if size > max_size_bytes:
        raise BadRequestException("File exceeds maximum allowed size")
