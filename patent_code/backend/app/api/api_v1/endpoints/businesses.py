from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import get_db
from backend.app.api.api_v1.dependencies import get_current_user, require_role
from backend.app.services.business_service import create_business_application, get_business_for_owner
from backend.app.schemas.pet_hotel import PetHotelRead
from backend.app.schemas.pet_hotel import PetHotelCreate
from backend.app.schemas.pet_hotel import PetHotelBase
from backend.app.schemas.pet_hotel import PetHotelRead
from backend.app.schemas.pet_hotel import PetHotelCreate
from backend.app.models.business import Business
from backend.app.models.pet_hotel import PetHotel
from sqlalchemy import select
from backend.app.models.reservation import Reservation


router = APIRouter()


@router.post("/businesses/apply")
async def apply_business(payload: dict, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    # Create a business application owned by current user
    b = await create_business_application(db, current_user.id, payload)
    return {"id": b.id, "status": b.status}


@router.get("/businesses/me")
async def my_business(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    b = await get_business_for_owner(db, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="No business registered for this user")
    return b


@router.get("/businesses/me/hotels")
async def my_business_hotels(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    b = await get_business_for_owner(db, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="No business registered for this user")
    r = await db.execute(select(PetHotel).where(PetHotel.business_id == b.id))
    return r.scalars().all()


@router.get("/businesses/me/reservations")
async def my_business_reservations(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    b = await get_business_for_owner(db, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="No business registered for this user")
    # get reservations for hotels under this business
    stmt = select(Reservation).join(PetHotel, Reservation.hotel_id == PetHotel.id).where(PetHotel.business_id == b.id)
    r = await db.execute(stmt)
    return r.scalars().all()
