import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient


from backend.app.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
from fastapi.testclient import TestClient
from backend.app.main import app


def test_ping():
    client = TestClient(app)
    r = client.get("/api/v1/health/ping")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
