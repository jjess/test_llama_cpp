import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import asyncio
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def db_session():
    """Mock database session."""
    session = MagicMock()
    return session


@pytest.fixture
def client(db_session):
    """Create test client with mocked DB."""
    with patch('src.database.get_db', return_value=db_session):
        with TestClient(app, raise_server_exceptions=False) as c:
            yield c
