# conftest.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, create_autospec
from sqlalchemy.orm import Session

from app.main import app
from app.db.database import get_db

@pytest.fixture(scope="function")
def mock_db():
    # Crée un mock de session SQLAlchemy
    mock = create_autospec(Session, instance=True)
    yield mock

@pytest.fixture(scope="function")
def client(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    yield TestClient(app)
    app.dependency_overrides.clear()