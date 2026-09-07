from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class PetHotelBase(BaseModel):
    name: str
    description: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    services: Optional[Dict[str, Any]]
    price_per_night: Optional[float]
    capacity: int
    working_hours: Optional[Dict[str, Any]]


class PetHotelCreate(PetHotelBase):
    pass


class PetHotelRead(PetHotelBase):
    id: int
    owner_id: Optional[int]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
