from fastapi import APIRouter

from backend.app.api.api_v1.endpoints import health, auth, animals, health_records, clinics

api_router = APIRouter()
api_router.include_router(health.router, prefix="", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(animals.router, prefix="", tags=["animals"])
api_router.include_router(health_records.router, prefix="", tags=["health_records"])
api_router.include_router(clinics.router, prefix="", tags=["clinics"])
