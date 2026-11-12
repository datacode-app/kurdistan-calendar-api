import pytest
from fastapi.testclient import TestClient

from api.core.rate_limiter import limiter
from api.main import app


@pytest.fixture()
def client():
    limiter.enabled = False
    return TestClient(app)
