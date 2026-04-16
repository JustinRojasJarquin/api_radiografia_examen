from typing import Optional

from sqlalchemy.orm import Session

from core.database.models.radiography_record import RadiographyRecord


class RadiographyRecordRepository:
    def create(self, db: Session, data: dict) -> RadiographyRecord:
        record = RadiographyRecord(**data)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def get_all(self, db: Session) -> list[RadiographyRecord]:
        return db.query(RadiographyRecord).order_by(RadiographyRecord.id.desc()).all()

    def get_by_id(self, db: Session, record_id: int) -> Optional[RadiographyRecord]:
        return (
            db.query(RadiographyRecord)
            .filter(RadiographyRecord.id == record_id)
            .first()
        )

    def update(
        self,
        db: Session,
        record: RadiographyRecord,
        data: dict
    ) -> RadiographyRecord:
        for key, value in data.items():
            setattr(record, key, value)

        db.commit()
        db.refresh(record)
        return record

    def delete(self, db: Session, record: RadiographyRecord) -> None:
        db.delete(record)
        db.commit()