from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String

from core.database.base import Base


class RadiographyRecord(Base):
    __tablename__ = "radiography_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_full_name = Column(String(255), nullable=False)
    patient_identifier = Column(String(100), nullable=False)
    clinical_reference = Column(String(500), nullable=False)
    study_date = Column(Date, nullable=False)
    image_url = Column(String(500), nullable=False)
    image_public_id = Column(String(255), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )