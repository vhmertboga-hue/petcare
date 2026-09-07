from fastapi import FastAPI
from backend.app.core.config import settings
from backend.app.api.api_v1.api import api_router
from backend.app.core.logging import configure_logging

configure_logging()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}

from fastapi import FastAPI
from backend.app.api.v1 import health, auth, animals
from backend.app.core.config import settings

app = FastAPI(title="PetCare API", version="0.1.0")

app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(animals.router, prefix="/api/v1/animals", tags=["animals"])


@app.on_event("startup")
def on_startup():
    # place for startup tasks (init DB connections, caches, etc.)
    if settings.debug:
        print("Starting in DEBUG mode")

