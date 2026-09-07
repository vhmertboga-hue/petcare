from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.api_v1.dependencies import get_current_user
from backend.app.db.session import get_db
from backend.app.schemas.health import VaccinationCreate, VaccinationRead, MedicationCreate, MedicationRead
from backend.app.services.health_service import create_vaccination, list_vaccinations, create_medication, list_medications
from backend.app.services.animal_service import get_animal

router = APIRouter()


@router.post("/animals/{animal_id}/vaccinations", response_model=VaccinationRead)
async def add_vaccination(animal_id: int, payload: VaccinationCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    animal = await get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    if animal.owner_id != current_user.id and not getattr(current_user, "is_superuser", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    v = await create_vaccination(db, animal_id, payload)
    return v


@router.get("/animals/{animal_id}/vaccinations", response_model=list[VaccinationRead])
async def get_vaccinations(animal_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    animal = await get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    if animal.owner_id != current_user.id and not getattr(current_user, "is_superuser", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return await list_vaccinations(db, animal_id)


@router.post("/animals/{animal_id}/medications", response_model=MedicationRead)
async def add_medication(animal_id: int, payload: MedicationCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    animal = await get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    if animal.owner_id != current_user.id and not getattr(current_user, "is_superuser", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    m = await create_medication(db, animal_id, payload)
    return m


@router.get("/animals/{animal_id}/medications", response_model=list[MedicationRead])
async def get_medications(animal_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    animal = await get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    if animal.owner_id != current_user.id and not getattr(current_user, "is_superuser", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return await list_medications(db, animal_id)
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}
