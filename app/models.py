from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    last_login = Column(DateTime, default=datetime.now())
