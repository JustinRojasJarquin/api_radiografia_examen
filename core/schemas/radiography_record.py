from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class RadiographyRecordBase(BaseModel):
    patient_full_name: str = Field(..., min_length=3, max_length=255)
    patient_identifier: str = Field(..., min_length=3, max_length=100)
    clinical_reference: str = Field(..., min_length=3, max_length=500)
    study_date: date
    image_url: str = Field(..., min_length=5, max_length=500)
    image_public_id: Optional[str] = Field(default=None, max_length=255)


class RadiographyRecordCreate(RadiographyRecordBase):
    created_by: int


class RadiographyRecordUpdate(BaseModel):
    patient_full_name: Optional[str] = Field(default=None, min_length=3, max_length=255)
    patient_identifier: Optional[str] = Field(default=None, min_length=3, max_length=100)
    clinical_reference: Optional[str] = Field(default=None, min_length=3, max_length=500)
    study_date: Optional[date] = None
    image_url: Optional[str] = Field(default=None, min_length=5, max_length=500)
    image_public_id: Optional[str] = Field(default=None, max_length=255)


class RadiographyRecordResponse(BaseModel):
    id: int
    patient_full_name: str
    patient_identifier: str
    clinical_reference: str
    study_date: date
    image_url: str
    image_public_id: Optional[str]
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)