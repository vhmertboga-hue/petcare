from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File as UploadFileType
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.api_v1.dependencies import get_current_user
from backend.app.db.session import get_db
from backend.app.schemas.animal import AnimalCreate, AnimalRead, AnimalPrivateRead, AnimalUpdate
from backend.app.services.animal_service import create_animal, get_animal, list_animals_for_owner, update_animal, delete_animal
from backend.app.services.file_service import save_file_for_animal

router = APIRouter()


@router.post("/animals", response_model=AnimalRead)
async def add_animal(payload: AnimalCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    animal = await create_animal(db, owner_id=current_user.id, payload=payload)
    return animal


@router.get("/animals", response_model=list[AnimalRead])
async def get_my_animals(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    animals = await list_animals_for_owner(db, current_user.id)
    return animals


@router.get("/animals/{animal_id}")
async def read_animal(animal_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    animal = await get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    if animal.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # hide microchip for non-owners
    if animal.owner_id == current_user.id or getattr(current_user, "is_superuser", False):
        return AnimalPrivateRead.from_orm(animal)
    return AnimalRead.from_orm(animal)


@router.patch("/animals/{animal_id}", response_model=AnimalRead)
async def patch_animal(animal_id: int, updates: AnimalUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    animal = await get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    if animal.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    updated = await update_animal(db, animal_id, updates)
    return updated


@router.delete("/animals/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_animal(animal_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    animal = await get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    if animal.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    await delete_animal(db, animal_id)
    return None


@router.post("/animals/{animal_id}/photos")
async def upload_photo(animal_id: int, file: UploadFileType = UploadFile(...), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    animal = await get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    if animal.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    content = await file.read()
    f = await save_file_for_animal(db, owner_id=current_user.id, animal_id=animal_id, filename=file.filename, content=content, mimetype=file.content_type)
    return {"id": f.id, "filename": f.filename, "url": f.url}
