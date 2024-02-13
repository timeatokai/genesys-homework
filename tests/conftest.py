import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.dependencies import get_db
from app.main import app

# Set up test database
DB_URL = "sqlite:///./sql_app_test.db"

engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def unique_email():
    yield f"test+{str(uuid.uuid4())}@test.com"


@pytest.fixture
def unique_username():
    yield str(uuid.uuid4())
