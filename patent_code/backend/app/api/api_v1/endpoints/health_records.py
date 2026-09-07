from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.api_v1.dependencies import get_current_user
from backend.app.db.session import get_db
from backend.app.services.storage_service import store_upload
from backend.app.models.health import Vaccination
from backend.app.models.file import File as FileModel
from backend.app.models.animal import Animal

router = APIRouter()


@router.post("/animals/{animal_id}/documents")
async def upload_document(animal_id: int, upload: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    # check animal ownership
    a = await db.get(Animal, animal_id)
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    if a.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    f = await store_upload(db, upload, owner_id=current_user.id)
    # create HealthDocument linking to file
    from backend.app.models.health import HealthDocument

    hd = HealthDocument(animal_id=animal_id, file_id=f.id, description=None)
    db.add(hd)
    await db.flush()
    await db.commit()
    await db.refresh(hd)
    return {"id": hd.id, "file_id": f.id}


@router.post("/animals/{animal_id}/vaccinations")
async def add_vaccination(animal_id: int, payload: dict, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    a = await db.get(Animal, animal_id)
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    if a.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    v = Vaccination(
        animal_id=animal_id,
        name=payload.get("name"),
        date=payload.get("date"),
        next_date=payload.get("next_date"),
        veterinarian_id=payload.get("veterinarian_id"),
        clinic=payload.get("clinic"),
        note=payload.get("note"),
    )
    db.add(v)
    await db.flush()
    await db.commit()
    await db.refresh(v)
    return {"id": v.id}
