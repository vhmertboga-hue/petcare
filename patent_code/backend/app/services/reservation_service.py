from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime

from backend.app.models.reservation import Reservation
from backend.app.models.pet_hotel import PetHotel


async def check_availability(db: AsyncSession, hotel_id: int, start: datetime, end: datetime) -> int:
    # count confirmed reservations overlapping the date range
    stmt = select(func.coalesce(func.sum(Reservation.guests), 0)).where(
        Reservation.hotel_id == hotel_id,
        Reservation.status.in_(["confirmed", "pending"]),
        Reservation.start_date < end,
        Reservation.end_date > start,
    )
    r = await db.execute(stmt)
    count = r.scalar() or 0
    return int(count)


async def create_reservation(db: AsyncSession, user_id: Optional[int], payload: Dict[str, Any]) -> Reservation:
    # load hotel capacity
    r = await db.execute(select(PetHotel).where(PetHotel.id == payload.get("hotel_id")))
    hotel = r.scalars().first()
    if not hotel:
        raise ValueError("Hotel not found")
    start = payload.get("start_date")
    end = payload.get("end_date")
    guests = int(payload.get("guests", 1))
    existing = await check_availability(db, hotel.id, start, end)
    if existing + guests > hotel.capacity:
        raise ValueError("Not enough capacity for requested dates")
    res = Reservation(user_id=user_id, hotel_id=hotel.id, pet_type=payload.get("pet_type"), pet_size=payload.get("pet_size"), start_date=start, end_date=end, guests=guests, status="pending")
    # compute price simple
    nights = max(1, (end - start).days)
    res.total_price = (hotel.price_per_night or 0.0) * nights * guests
    db.add(res)
    await db.flush()
    await db.commit()
    await db.refresh(res)
    return res
