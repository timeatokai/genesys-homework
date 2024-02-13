from datetime import datetime, timedelta, timezone
from typing import Optional, Dict

from jose import jwt
from passlib.context import CryptContext

from app import models

SECRET_KEY = "6c3957f5cdc5673ee799835f872cff2c217cd1b6e2827032fb90d80a3adeb026"
ALGORITHM = "HS256"

password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return password_ctx.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_ctx.verify(plain_password, hashed_password)


def authenticate_user(user: models.User, password: str) -> bool:
    if not (user and verify_password(password, user.hashed_password)):
        return False
    return True


def create_access_token(data: Dict, expires_minutes: Optional[int] = 15) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
