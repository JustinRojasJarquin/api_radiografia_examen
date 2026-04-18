from __future__ import annotations

from typing import Any

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def parse_positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default

    if parsed < 1:
        return default

    return parsed


def get_pagination_params(query_params: dict[str, Any]) -> tuple[int, int]:
    page = parse_positive_int(query_params.get("page"), DEFAULT_PAGE)
    page_size = parse_positive_int(query_params.get("page_size"), DEFAULT_PAGE_SIZE)

    if page_size > MAX_PAGE_SIZE:
        page_size = MAX_PAGE_SIZE

    return page, page_size


def paginate_query(query, page: int, page_size: int):
    offset = (page - 1) * page_size
    return query.limit(page_size).offset(offset)
