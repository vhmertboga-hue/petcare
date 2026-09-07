from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AdoptionBase(BaseModel):
    species: str
    breed: Optional[str]
    gender: Optional[str]
    age: Optional[str]
    description: Optional[str]
    color: Optional[str]
    sterilized: Optional[bool]
    vaccinated: Optional[bool]
    location_region: Optional[str]
    contact_method: Optional[str]


class AdoptionCreate(AdoptionBase):
    pass


class AdoptionUpdate(BaseModel):
    status: Optional[str]
    is_closed: Optional[bool]


class AdoptionRead(AdoptionBase):
    id: int
    owner_id: Optional[int]
    status: str
    is_closed: bool
    created_at: Optional[str]

    class Config:
        orm_mode = True
