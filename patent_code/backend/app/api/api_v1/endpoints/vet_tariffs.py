from fastapi import APIRouter, Depends, UploadFile, File as UploadFileType, HTTPException
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.api_v1.dependencies import get_current_user, require_role
from backend.app.db.session import get_db
from backend.app.schemas.vet_tariff import VetTariffCreate, VetTariffRead, VetTariffUpdate
from backend.app.services.vet_tariff_service import create_tariff, update_tariff, delete_tariff, get_tariff, list_tariffs
from backend.app.services.file_service import save_file_for_animal

router = APIRouter()


@router.get("/tariffs", response_model=list[VetTariffRead])
async def read_tariffs(province: Optional[str] = None, year: Optional[int] = None, service_name: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    filters = {"province": province, "year": year, "service_name": service_name}
    res = await list_tariffs(db, filters)
    return res


@router.get("/tariffs/{tariff_id}", response_model=VetTariffRead)
async def read_tariff(tariff_id: int, db: AsyncSession = Depends(get_db)):
    t = await get_tariff(db, tariff_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return t


# Admin endpoints
@router.post("/tariffs", response_model=VetTariffRead, dependencies=[Depends(require_role("admin"))])
async def post_tariff(payload: VetTariffCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    t = await create_tariff(db, current_user.id, payload.dict())
    return t


@router.put("/tariffs/{tariff_id}", response_model=VetTariffRead, dependencies=[Depends(require_role("admin"))])
async def put_tariff(tariff_id: int, payload: VetTariffUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    t = await update_tariff(db, current_user.id, tariff_id, payload.dict(exclude_unset=True))
    if not t:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return t


@router.delete("/tariffs/{tariff_id}", dependencies=[Depends(require_role("admin"))])
async def remove_tariff(tariff_id: int, soft: Optional[bool] = True, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    ok = await delete_tariff(db, current_user.id, tariff_id, soft=soft)
    if not ok:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return {"ok": True}


@router.post("/tariffs/{tariff_id}/upload", dependencies=[Depends(require_role("admin"))])
async def upload_tariff_source(tariff_id: int, file: UploadFile, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    content = await file.read()
    # reuse file_service saving function but set owner to current_user and tariff specific
    f = await save_file_for_animal(db, current_user.id, None, file.filename, content, mimetype=file.content_type)
    # associate file with tariff record
    from backend.app.models.vet_tariff import VetTariff
    from sqlalchemy import select
    r = await db.execute(select(VetTariff).where(VetTariff.id == tariff_id))
    t = r.scalars().first()
    if not t:
        raise HTTPException(status_code=404, detail="Tariff not found")
    t.source_document_id = f.id
    await db.commit()
    return {"file_id": f.id}
