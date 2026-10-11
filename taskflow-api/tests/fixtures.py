import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def db_session():
    """Create mock database session."""
    session = MagicMock()
    return session


@pytest.fixture
def client(db_session):
    """Create test client with mocked DB."""
    with patch('src.main.get_db', return_value=db_session):
        with TestClient(app, raise_server_exceptions=False) as c:
            yield c
