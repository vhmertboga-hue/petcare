from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.models.vet_tariff import VetTariff
from backend.app.models.audit import AuditLog


async def create_tariff(db: AsyncSession, user_id: Optional[int], payload: Dict[str, Any]):
    t = VetTariff(**payload)
    db.add(t)
    await db.flush()
    # audit
    a = AuditLog(user_id=user_id, action="tariff.create", details=f"Created tariff id={t.id}")
    db.add(a)
    await db.commit()
    await db.refresh(t)
    return t


async def update_tariff(db: AsyncSession, user_id: Optional[int], tariff_id: int, payload: Dict[str, Any]):
    r = await db.execute(select(VetTariff).where(VetTariff.id == tariff_id))
    t = r.scalars().first()
    if not t:
        return None
    for k, v in payload.items():
        setattr(t, k, v)
    a = AuditLog(user_id=user_id, action="tariff.update", details=f"Updated tariff id={t.id}")
    db.add(a)
    await db.commit()
    await db.refresh(t)
    return t


async def delete_tariff(db: AsyncSession, user_id: Optional[int], tariff_id: int, soft=True):
    r = await db.execute(select(VetTariff).where(VetTariff.id == tariff_id))
    t = r.scalars().first()
    if not t:
        return False
    if soft:
        t.active = False
    else:
        await db.delete(t)
    a = AuditLog(user_id=user_id, action="tariff.delete", details=f"Deleted tariff id={tariff_id} soft={soft}")
    db.add(a)
    await db.commit()
    return True


async def get_tariff(db: AsyncSession, tariff_id: int):
    r = await db.execute(select(VetTariff).where(VetTariff.id == tariff_id))
    return r.scalars().first()


async def list_tariffs(db: AsyncSession, filters: Dict = None) -> List[VetTariff]:
    filters = filters or {}
    stmt = select(VetTariff)
    if filters.get("province"):
        stmt = stmt.where(VetTariff.province == filters.get("province"))
    if filters.get("year"):
        stmt = stmt.where(VetTariff.year == int(filters.get("year")))
    if filters.get("service_name"):
        stmt = stmt.where(VetTariff.service_name.ilike(f"%{filters.get('service_name')}%"))
    if filters.get("active") is not None:
        stmt = stmt.where(VetTariff.active == bool(filters.get("active")))
    r = await db.execute(stmt)
    return r.scalars().all()
