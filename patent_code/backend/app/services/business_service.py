from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional, Dict, Any

from backend.app.models.business import Business


async def create_business_application(db: AsyncSession, owner_id: int, payload: Dict[str, Any]) -> Business:
    b = Business(owner_id=owner_id, name=payload.get("name"), type=payload.get("type"), description=payload.get("description"), address=payload.get("address"), latitude=payload.get("latitude"), longitude=payload.get("longitude"), phone=payload.get("phone"), working_hours=payload.get("working_hours"), services=payload.get("services"), prices=payload.get("prices"))
    db.add(b)
    await db.flush()
    await db.commit()
    await db.refresh(b)
    return b


async def get_business_for_owner(db: AsyncSession, owner_id: int) -> Optional[Business]:
    r = await db.execute(select(Business).where(Business.owner_id == owner_id))
    return r.scalars().first()


async def update_business_status(db: AsyncSession, business_id: int, status: str) -> Optional[Business]:
    await db.execute(update(Business).where(Business.id == business_id).values(status=status))
    await db.commit()
    r = await db.execute(select(Business).where(Business.id == business_id))
    return r.scalars().first()
