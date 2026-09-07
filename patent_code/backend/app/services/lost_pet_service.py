from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from math import radians, cos, sin, asin, sqrt

from backend.app.models.lost_pet import LostPet
from backend.app.models.user_location import UserLocation
from backend.app.models.notification import Notification


def haversine_km(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c


async def create_lost_pet(db: AsyncSession, owner_id: Optional[int], payload: Dict[str, Any]):
    lp = LostPet(owner_id=owner_id, **payload)
    db.add(lp)
    await db.flush()
    # enqueue nearby notifications if location provided
    if lp.latitude and lp.longitude:
        await notify_nearby(db, lp)
    await db.commit()
    await db.refresh(lp)
    return lp


async def update_lost_pet(db: AsyncSession, pet_id: int, payload: Dict[str, Any]):
    r = await db.execute(select(LostPet).where(LostPet.id == pet_id))
    lp = r.scalars().first()
    if not lp:
        return None
    for k, v in payload.items():
        setattr(lp, k, v)
    await db.commit()
    await db.refresh(lp)
    return lp


async def notify_nearby(db: AsyncSession, lost_pet: LostPet, radius_km: float = 5.0):
    # find opt-in user locations within radius and create Notification rows
    if not (lost_pet.latitude and lost_pet.longitude):
        return 0
    r = await db.execute(select(UserLocation))
    locations = r.scalars().all()
    count = 0
    for loc in locations:
        if not loc.opt_in:
            continue
        dist = haversine_km(lost_pet.longitude, lost_pet.latitude, loc.longitude, loc.latitude)
        if dist <= radius_km:
            notif = Notification(user_id=loc.user_id, type="lost_pet_nearby", payload={"lost_pet_id": lost_pet.id, "distance_km": dist})
            db.add(notif)
            count += 1
    await db.commit()
    return count


async def list_lost_pets(db: AsyncSession, filters: Dict = None) -> List[LostPet]:
    filters = filters or {}
    stmt = select(LostPet)
    if filters.get("species"):
        stmt = stmt.where(LostPet.species == filters.get("species"))
    if filters.get("is_published") is not None:
        stmt = stmt.where(LostPet.is_published == bool(filters.get("is_published")))
    r = await db.execute(stmt)
    return r.scalars().all()
