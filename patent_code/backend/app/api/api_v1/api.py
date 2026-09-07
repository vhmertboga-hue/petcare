from fastapi import APIRouter

from backend.app.api.api_v1.endpoints import health, auth, animals, health_records, clinics, vet_tariffs, lost_pets, adoptions, ai, hotels, reservations, businesses, admin_businesses

api_router = APIRouter()
api_router.include_router(health.router, prefix="", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(animals.router, prefix="", tags=["animals"])
api_router.include_router(health_records.router, prefix="", tags=["health_records"])
api_router.include_router(clinics.router, prefix="", tags=["clinics"])
api_router.include_router(vet_tariffs.router, prefix="/api", tags=["vet_tariffs"])
api_router.include_router(lost_pets.router, prefix="/api", tags=["lost_pets"])
api_router.include_router(adoptions.router, prefix="/api", tags=["adoptions"])
api_router.include_router(ai.router, prefix="/api", tags=["ai"])
api_router.include_router(hotels.router, prefix="/api", tags=["hotels"])
api_router.include_router(reservations.router, prefix="/api", tags=["reservations"])
api_router.include_router(businesses.router, prefix="/api", tags=["businesses"])
api_router.include_router(admin_businesses.router, prefix="/api", tags=["admin-businesses"])
