from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backend.app.db.session import get_db
from backend.app.api.api_v1.dependencies import get_current_user, require_role
from backend.app.schemas.pet_hotel import PetHotelCreate, PetHotelRead
from backend.app.services.reservation_service import check_availability
from backend.app.models.pet_hotel import PetHotel
from sqlalchemy import select

router = APIRouter()


@router.post("/hotels", response_model=PetHotelRead, dependencies=[Depends(require_role("BUSINESS"))])
async def create_hotel(payload: PetHotelCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    # attach to user's business when available
    from backend.app.services.business_service import get_business_for_owner
    b = await get_business_for_owner(db, current_user.id)
    business_id = b.id if b else None
    h = PetHotel(owner_id=current_user.id, business_id=business_id, **payload.dict())
    db.add(h)
    await db.flush()
    await db.commit()
    await db.refresh(h)
    return h


@router.get("/hotels", response_model=list[PetHotelRead])
async def list_hotels(db: AsyncSession = Depends(get_db), species: Optional[str] = None):
    r = await db.execute(select(PetHotel))
    return r.scalars().all()


@router.get("/hotels/{hotel_id}", response_model=PetHotelRead)
async def get_hotel(hotel_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(PetHotel).where(PetHotel.id == hotel_id))
    h = r.scalars().first()
    if not h:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return h


@router.get("/hotels/{hotel_id}/availability")
async def hotel_availability(hotel_id: int, start: Optional[str] = None, end: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    # expects ISO dates
    from datetime import datetime
    if not start or not end:
        raise HTTPException(status_code=400, detail="start and end required")
    s = datetime.fromisoformat(start)
    e = datetime.fromisoformat(end)
    used = await check_availability(db, hotel_id, s, e)
    r = await db.execute(select(PetHotel).where(PetHotel.id == hotel_id))
    hotel = r.scalars().first()
    return {"capacity": hotel.capacity, "booked": used, "available": max(0, hotel.capacity - used)}
