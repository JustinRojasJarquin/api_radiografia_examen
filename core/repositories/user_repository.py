from typing import Optional

from sqlalchemy.orm import Session

from core.database.models.user import User


class UserRepository:
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        normalized_email = email.strip().lower()
        return db.query(User).filter(User.email == normalized_email).first()

    def create(self, db: Session, data: dict) -> User:
        user = User(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user: User, data: dict) -> User:
        for key, value in data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    def get_or_create(self, db: Session, *, email: str, full_name: str) -> tuple[User, bool]:
        user = self.get_by_email(db, email)
        if user:
            return user, False

        user = self.create(
            db,
            {
                "email": email.strip().lower(),
                "full_name": full_name.strip() or email.strip().lower(),
                "is_active": True,
            },
        )
        return user, True
