from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.api.api_v1.dependencies import get_current_user, require_role
from backend.app.schemas.adoption import AdoptionCreate, AdoptionRead, AdoptionUpdate
from backend.app.services.adoption_service import create_adoption, update_adoption, list_adoptions

router = APIRouter()


@router.post("/adoptions", response_model=AdoptionRead)
async def post_adoption(payload: AdoptionCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    a = await create_adoption(db, current_user.id, payload.dict())
    return a


@router.put("/adoptions/{adoption_id}", response_model=AdoptionRead)
async def put_adoption(adoption_id: int, payload: AdoptionUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    a = await update_adoption(db, adoption_id, payload.dict(exclude_unset=True))
    if not a:
        raise HTTPException(status_code=404, detail="Adoption not found")
    return a


@router.get("/adoptions", response_model=list[AdoptionRead])
async def get_adoptions(species: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    items = await list_adoptions(db, {"species": species})
    return items
