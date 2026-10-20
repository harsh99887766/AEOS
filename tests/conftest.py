import pytest
from fastapi.testclient import TestClient

from aeos.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
