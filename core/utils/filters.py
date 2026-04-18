from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Query


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _parse_date(value: Any):
    if not value:
        return None

    try:
        return datetime.fromisoformat(str(value)).date()
    except ValueError:
        return None


def apply_record_filters(query: Query, model, params: dict[str, Any]) -> Query:
    patient_full_name = _normalize_text(params.get("patient_full_name"))
    patient_identifier = _normalize_text(params.get("patient_identifier"))
    clinical_reference = _normalize_text(params.get("clinical_reference"))
    study_date = _parse_date(params.get("study_date"))
    search = _normalize_text(params.get("search"))
    order_by = _normalize_text(params.get("order_by"))

    if patient_full_name:
        query = query.filter(model.patient_full_name.ilike(f"%{patient_full_name}%"))

    if patient_identifier:
        query = query.filter(model.patient_identifier.ilike(f"%{patient_identifier}%"))

    if clinical_reference:
        query = query.filter(model.clinical_reference.ilike(f"%{clinical_reference}%"))

    if study_date:
        query = query.filter(model.study_date == study_date)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            model.patient_full_name.ilike(search_pattern)
            | model.patient_identifier.ilike(search_pattern)
            | model.clinical_reference.ilike(search_pattern)
        )

    if order_by:
        descending = order_by.startswith("-")
        field_name = order_by[1:] if descending else order_by

        if hasattr(model, field_name):
            field = getattr(model, field_name)
            query = query.order_by(field.desc() if descending else field)

    return query
