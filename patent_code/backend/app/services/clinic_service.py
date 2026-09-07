from typing import List, Optional, Dict, Any
from math import radians, cos, sin, asin, sqrt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text

from backend.app.models.vet import Vet
from backend.app.models.clinic_review import ClinicReview


def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km


async def create_clinic(db: AsyncSession, data: Dict[str, Any]) -> Vet:
    v = Vet(**data)
    db.add(v)
    await db.flush()
    await db.commit()
    await db.refresh(v)
    return v


async def get_clinic(db: AsyncSession, clinic_id: int) -> Optional[Vet]:
    r = await db.execute(select(Vet).where(Vet.id == clinic_id))
    return r.scalars().first()


async def list_clinics(db: AsyncSession, lat: Optional[float] = None, lon: Optional[float] = None, filters: Dict = None) -> List[Dict]:
    """List clinics. If PostGIS is available on the DB, prefer DB-side distance calculation for performance; otherwise fallback to in-Python Haversine."""
    filters = filters or {}

    # Try PostGIS approach first
    try:
        if lat is not None and lon is not None:
            # Use ST_DistanceSphere for accurate meters distance
            stmt = select(Vet, func.ST_DistanceSphere(Vet.location, func.ST_MakePoint(lon, lat)).label("distance_m"))
            # Apply simple filters in SQL
            if filters.get("emergency"):
                stmt = stmt.where(Vet.emergency == True)
            if filters.get("open_24_7"):
                stmt = stmt.where(Vet.open_24_7 == True)
            if filters.get("open"):
                stmt = stmt.where(Vet.is_open == True)
            stmt = stmt.order_by(text("distance_m"))
            res = await db.execute(stmt)
            rows = res.all()
            results = []
            for v, dist in rows:
                results.append({"clinic": v, "distance_km": None if dist is None else float(dist) / 1000.0})
            return results
    except Exception:
        # if anything fails (no PostGIS, geometry type mismatch, etc.), fallback to Python method
        pass

    # Fallback: load clinics and compute distances in Python
    r = await db.execute(select(Vet))
    vets = r.scalars().all()

    results = []
    for v in vets:
        item = {
            "clinic": v,
            "distance_km": None
        }
        if lat is not None and lon is not None and v.latitude is not None and v.longitude is not None:
            item["distance_km"] = haversine(lon, lat, v.longitude, v.latitude)
        results.append(item)

    # apply simple filters
    if filters.get("open"):
        results = [r for r in results if getattr(r["clinic"], "is_open", True)]
    if filters.get("emergency"):
        results = [r for r in results if getattr(r["clinic"], "emergency", False)]
    if filters.get("open_24_7"):
        results = [r for r in results if getattr(r["clinic"], "open_24_7", False)]

    # sort by distance if provided
    if lat is not None and lon is not None:
        results = sorted(results, key=lambda r: (r["distance_km"] is None, r["distance_km"]))

    return results


async def add_review(db: AsyncSession, clinic_id: int, user_id: Optional[int], payload: Dict) -> ClinicReview:
    rev = ClinicReview(clinic_id=clinic_id, user_id=user_id, rating=payload.get("rating"), title=payload.get("title"), body=payload.get("body"))
    db.add(rev)
    await db.flush()
    await db.commit()
    await db.refresh(rev)
    return rev
