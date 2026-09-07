from typing import Optional, List
from pydantic import BaseModel


class ClinicCreate(BaseModel):
    name: str
    clinic: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    working_hours: Optional[dict]
    emergency: Optional[bool] = False
    open_24_7: Optional[bool] = False
    services: Optional[str]
    is_open: Optional[bool] = True


class ClinicRead(BaseModel):
    id: int
    name: str
    clinic: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    emergency: Optional[bool]
    open_24_7: Optional[bool]
    services: Optional[str]
    is_open: Optional[bool]
    rating: Optional[float]

    class Config:
        orm_mode = True


class ClinicReviewCreate(BaseModel):
    rating: float
    title: Optional[str]
    body: Optional[str]


class ClinicReviewRead(BaseModel):
    id: int
    clinic_id: int
    user_id: Optional[int]
    rating: float
    title: Optional[str]
    body: Optional[str]
    created_at: Optional[str]

    class Config:
        orm_mode = True
