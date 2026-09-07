import pytest
from httpx import AsyncClient

from backend.app.main import app


@pytest.mark.asyncio
async def test_create_animal_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # register
        r = await ac.post("/api/v1/auth/register", json={"email": "owner@example.com", "password": "secret"})
        assert r.status_code == 200

        r2 = await ac.post("/api/v1/auth/login", json={"email": "owner@example.com", "password": "secret"})
        assert r2.status_code == 200
        tok = r2.json()
        access = tok.get("access_token")
        assert access

        headers = {"Authorization": f"Bearer {access}"}
        payload = {"name": "Rex", "species": "dog"}
        r3 = await ac.post("/api/v1/animals", json=payload, headers=headers)
        assert r3.status_code == 200
        data = r3.json()
        assert data.get("name") == "Rex"
