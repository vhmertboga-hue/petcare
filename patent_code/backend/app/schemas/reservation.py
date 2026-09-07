from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReservationCreate(BaseModel):
    hotel_id: int
    pet_type: str
    pet_size: Optional[str]
    start_date: datetime
    end_date: datetime
    guests: int = 1
    pickup: Optional[bool] = False


class ReservationRead(BaseModel):
    id: int
    hotel_id: int
    user_id: Optional[int]
    pet_type: str
    pet_size: Optional[str]
    start_date: datetime
    end_date: datetime
    guests: int
    total_price: Optional[float]
    status: str

    class Config:
        orm_mode = True
