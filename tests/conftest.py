import pytest
from httpx import ASGITransport, AsyncClient

from src import app
from src.core.database import get_db

BASE_URL = "http://test/api/v1"


@pytest.fixture
async def client():
    async def override_get_db():
        yield None

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=BASE_URL
    ) as client:
        yield client

    app.dependency_overrides.clear()
