from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from core.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(254), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    @property
    def first_name(self) -> str:
        return self.full_name.strip().split(" ", 1)[0] if self.full_name else ""

    @property
    def last_name(self) -> str:
        if not self.full_name or " " not in self.full_name.strip():
            return ""
        return self.full_name.strip().split(" ", 1)[1]
