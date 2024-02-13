from typing import List, Optional
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth_utils import get_password_hash


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, name: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.name == name).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> Optional[models.User]:
    hashed_password = get_password_hash(user.password.get_secret_value())
    db_user = models.User(
        name=user.name, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Optional[models.User]:
    update_data = dict(user)
    if new_password := update_data.pop("password", None):
        update_data["hashed_password"] = get_password_hash(
            new_password.get_secret_value()
        )

    db_query = db.query(models.User).filter(models.User.id == user_id)
    db_query.update(update_data)
    db.commit()
    db.refresh(db_query.first())
    return db_query.first()


def delete_user(db: Session, user_id: int) -> int:
    db.delete(db.get(models.User, user_id))
    db.commit()
    return user_id


def list_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()
