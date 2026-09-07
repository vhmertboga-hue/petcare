from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LostPetBase(BaseModel):
    name: Optional[str]
    species: str
    breed: Optional[str]
    gender: Optional[str]
    age: Optional[str]
    color: Optional[str]
    distinguishing_features: Optional[str]
    missing_date: Optional[datetime]
    missing_region: Optional[str]
    description: Optional[str]
    contact_method: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    show_exact_location: Optional[bool] = False


class LostPetCreate(LostPetBase):
    pass


class LostPetUpdate(BaseModel):
    name: Optional[str]
    breed: Optional[str]
    gender: Optional[str]
    age: Optional[str]
    color: Optional[str]
    distinguishing_features: Optional[str]
    missing_date: Optional[datetime]
    missing_region: Optional[str]
    description: Optional[str]
    contact_method: Optional[str]
    is_published: Optional[bool]
    is_found: Optional[bool]
    is_closed: Optional[bool]
    latitude: Optional[float]
    longitude: Optional[float]
    show_exact_location: Optional[bool]


class LostPetRead(LostPetBase):
    id: int
    owner_id: Optional[int]
    is_published: bool
    is_found: bool
    is_closed: bool
    created_at: Optional[str]

    class Config:
        orm_mode = True
