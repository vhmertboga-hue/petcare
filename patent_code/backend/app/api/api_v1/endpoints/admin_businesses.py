from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import get_db
from backend.app.api.api_v1.dependencies import require_role
from backend.app.services.business_service import update_business_status
from sqlalchemy import select
from backend.app.models.business import Business

router = APIRouter()


@router.get("/admin/businesses/pending", dependencies=[Depends(require_role("admin"))])
async def list_pending(db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Business).where(Business.status == "pending"))
    return r.scalars().all()


@router.post("/admin/businesses/{business_id}/status", dependencies=[Depends(require_role("admin"))])
async def set_status(business_id: int, payload: dict, db: AsyncSession = Depends(get_db)):
    status = payload.get("status")
    if status not in ["pending", "verified", "rejected", "suspended"]:
        raise HTTPException(status_code=400, detail="invalid status")
    b = await update_business_status(db, business_id, status)
    if not b:
        raise HTTPException(status_code=404, detail="business not found")
    return {"id": b.id, "status": b.status}
