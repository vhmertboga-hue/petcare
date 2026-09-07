from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.models.adoption import Adoption
from backend.app.models.audit import AuditLog


async def create_adoption(db: AsyncSession, owner_id: Optional[int], payload: Dict[str, Any]):
    a = Adoption(owner_id=owner_id, **payload)
    db.add(a)
    await db.flush()
    al = AuditLog(user_id=owner_id, action="adoption.create", details=f"Created adoption id={a.id}")
    db.add(al)
    await db.commit()
    await db.refresh(a)
    return a


async def update_adoption(db: AsyncSession, adoption_id: int, payload: Dict[str, Any]):
    r = await db.execute(select(Adoption).where(Adoption.id == adoption_id))
    a = r.scalars().first()
    if not a:
        return None
    for k, v in payload.items():
        setattr(a, k, v)
    al = AuditLog(user_id=None, action="adoption.update", details=f"Updated adoption id={a.id}")
    db.add(al)
    await db.commit()
    await db.refresh(a)
    return a


async def list_adoptions(db: AsyncSession, filters: Dict = None) -> List[Adoption]:
    filters = filters or {}
    stmt = select(Adoption)
    if filters.get("species"):
        stmt = stmt.where(Adoption.species == filters.get("species"))
    if filters.get("sterilized") is not None:
        stmt = stmt.where(Adoption.sterilized == bool(filters.get("sterilized")))
    r = await db.execute(stmt)
    return r.scalars().all()
