from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.api_v1.dependencies import get_current_user
from backend.app.db.session import get_db
from backend.app.schemas.animal import AnimalCreate, AnimalRead
from backend.app.services.animal_service import create_animal, get_animal

router = APIRouter()


@router.post("/animals", response_model=AnimalRead)
async def add_animal(payload: AnimalCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    # only authenticated users can add animals
    animal = await create_animal(db, owner_id=current_user.id, payload=payload)
    return animal


@router.get("/animals/{animal_id}", response_model=AnimalRead)
async def read_animal(animal_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    animal = await get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    if animal.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return animal
