from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import get_db
from backend.app.api.api_v1.dependencies import get_current_user
from backend.app.schemas.reservation import ReservationCreate, ReservationRead
from backend.app.services.reservation_service import create_reservation

router = APIRouter()


@router.post("/reservations", response_model=ReservationRead)
async def post_reservation(payload: ReservationCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        res = await create_reservation(db, current_user.id, payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return res
