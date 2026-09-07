from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.api_v1.dependencies import get_current_user
from backend.app.db.session import get_db
from backend.app.schemas.clinic import ClinicRead, ClinicReviewCreate, ClinicReviewRead
from backend.app.services.clinic_service import list_clinics, get_clinic, add_review

router = APIRouter()


@router.get("/clinics", response_model=list[ClinicRead])
async def search_clinics(lat: Optional[float] = Query(None), lon: Optional[float] = Query(None), open: Optional[bool] = Query(None), emergency: Optional[bool] = Query(None), open_24_7: Optional[bool] = Query(None), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    filters = {"open": open, "emergency": emergency, "open_24_7": open_24_7}
    results = await list_clinics(db, lat=lat, lon=lon, filters=filters)
    # return only clinic objects for response
    clinics = [r["clinic"] for r in results]
    return clinics


@router.get("/clinics/{clinic_id}", response_model=ClinicRead)
async def read_clinic(clinic_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    c = await get_clinic(db, clinic_id)
    if not c:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return c


@router.post("/clinics/{clinic_id}/reviews", response_model=ClinicReviewRead)
async def post_review(clinic_id: int, payload: ClinicReviewCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    rev = await add_review(db, clinic_id, getattr(current_user, "id", None), payload.dict())
    return rev


@router.get("/emergency/nearby")
async def emergency_nearby(lat: Optional[float] = Query(None), lon: Optional[float] = Query(None), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """Return nearest emergency clinics with phone and directions (one-touch data)."""
    results = await list_clinics(db, lat=lat, lon=lon, filters={"emergency": True})
    # prepare one-touch payloads: phone, tel link, google directions url, osm url
    out = []
    for r in results[:10]:
        c = r["clinic"]
        item = {
            "id": c.id,
            "name": c.name,
            "phone": c.phone,
            "tel_link": f"tel:{c.phone}" if c.phone else None,
            "google_maps_directions": None,
            "osm_link": None,
            "distance_km": r.get("distance_km"),
        }
        if lat is not None and lon is not None and c.latitude and c.longitude:
            item["google_maps_directions"] = f"https://www.google.com/maps/dir/?api=1&origin={lat},{lon}&destination={c.latitude},{c.longitude}&travelmode=driving"
            item["osm_link"] = f"https://www.openstreetmap.org/directions?from={lat},{lon}&to={c.latitude},{c.longitude}"
        out.append(item)
    return out
