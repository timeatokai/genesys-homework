from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, SecretStr


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=128, strip_whitespace=True)
    email: EmailStr


class UserCreate(UserBase):
    password: SecretStr


class UserUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=128, strip_whitespace=True, default=None)
    email: EmailStr = None
    password: SecretStr = None


class User(UserBase):
    id: int
    last_login: datetime = Field(default=None)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "name": "username",
                    "email": "example@example.com",
                    "password": "password",
                    "last_login": datetime.now(),
                }
            ]
        },
    }
