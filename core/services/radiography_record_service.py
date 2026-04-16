from core.repositories.radiography_record_repository import RadiographyRecordRepository
from core.schemas.radiography_record import (
    RadiographyRecordCreate,
    RadiographyRecordUpdate,
)


class RadiographyRecordService:
    def __init__(self) -> None:
        self.repository = RadiographyRecordRepository()

    def create_record(self, db, payload: RadiographyRecordCreate):
        return self.repository.create(db, payload.model_dump())

    def list_records(self, db):
        return self.repository.get_all(db)

    def get_record_detail(self, db, record_id: int):
        record = self.repository.get_by_id(db, record_id)
        if not record:
            raise ValueError("Radiography record not found")
        return record

    def update_record(self, db, record_id: int, payload: RadiographyRecordUpdate):
        record = self.repository.get_by_id(db, record_id)
        if not record:
            raise ValueError("Radiography record not found")

        update_data = payload.model_dump(exclude_unset=True)
        return self.repository.update(db, record, update_data)

    def delete_record(self, db, record_id: int):
        record = self.repository.get_by_id(db, record_id)
        if not record:
            raise ValueError("Radiography record not found")

        self.repository.delete(db, record)
        return {"message": "Radiography record deleted successfully"}