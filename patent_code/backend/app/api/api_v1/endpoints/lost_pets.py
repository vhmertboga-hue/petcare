from fastapi import APIRouter, Depends, HTTPException, UploadFile
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.api.api_v1.dependencies import get_current_user, require_role
from backend.app.schemas.lost_pet import LostPetCreate, LostPetRead, LostPetUpdate
from backend.app.services.lost_pet_service import create_lost_pet, update_lost_pet, list_lost_pets
from backend.app.services.file_service import save_file_for_animal

router = APIRouter()


@router.post("/lost_pets", response_model=LostPetRead)
async def post_lost_pet(payload: LostPetCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    lp = await create_lost_pet(db, current_user.id, payload.dict())
    return lp


@router.put("/lost_pets/{pet_id}", response_model=LostPetRead)
async def put_lost_pet(pet_id: int, payload: LostPetUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    lp = await update_lost_pet(db, pet_id, payload.dict(exclude_unset=True))
    if not lp:
        raise HTTPException(status_code=404, detail="Lost post not found")
    return lp


@router.get("/lost_pets", response_model=list[LostPetRead])
async def get_lost_pets(species: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    items = await list_lost_pets(db, {"species": species, "is_published": True})
    return items


@router.post("/lost_pets/{pet_id}/upload_photo")
async def upload_lost_pet_photo(pet_id: int, file: UploadFile, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    content = await file.read()
    f = await save_file_for_animal(db, current_user.id, None, file.filename, content, mimetype=file.content_type)
    # associate with lost pet
    from backend.app.models import LostPet
    from sqlalchemy import select
    r = await db.execute(select(LostPet).where(LostPet.id == pet_id))
    lp = r.scalars().first()
    if not lp:
        raise HTTPException(status_code=404, detail="Lost post not found")
    f.lost_pet_id = pet_id
    await db.commit()
    return {"file_id": f.id}
