from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String

from core.database.base import Base


class RadiographyRecord(Base):
    __tablename__ = "radiography_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_full_name = Column(String, nullable=False)
    patient_identifier = Column(String, nullable=False)
    clinical_reference = Column(String, nullable=False)
    study_date = Column(Date, nullable=False)
    image_url = Column(String, nullable=False)
    image_public_id = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)