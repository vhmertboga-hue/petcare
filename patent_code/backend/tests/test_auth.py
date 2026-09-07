import pytest
from httpx import AsyncClient

from backend.app.main import app


@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/auth/register", json={"email": "test@example.com", "password": "secret"})
        assert r.status_code == 200
        data = r.json()
        assert data.get("email") == "test@example.com"

        r2 = await ac.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "secret"})
        assert r2.status_code == 200
        tok = r2.json()
        assert "access_token" in tok and "refresh_token" in tok
from fastapi.testclient import TestClient
from backend.app.main import app
import pytest


client = TestClient(app)


def test_register_and_login():
    email = "testuser@example.com"
    pw = "strongpassword"
    r = client.post("/api/v1/auth/register", json={"email": email, "password": pw})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data

    r2 = client.post("/api/v1/auth/login", json={"email": email, "password": pw})
    assert r2.status_code == 200
    d2 = r2.json()
    assert "access_token" in d2
