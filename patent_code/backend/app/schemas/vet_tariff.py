from typing import Optional
from pydantic import BaseModel
from datetime import date


class VetTariffBase(BaseModel):
    province: str
    chamber: Optional[str]
    year: int
    start_date: Optional[date]
    end_date: Optional[date]
    service_name: str
    service_category: Optional[str]
    official_amount: Optional[float]
    unit: Optional[str]
    source: Optional[str]
    active: Optional[bool] = True


class VetTariffCreate(VetTariffBase):
    pass


class VetTariffUpdate(BaseModel):
    province: Optional[str]
    chamber: Optional[str]
    year: Optional[int]
    start_date: Optional[date]
    end_date: Optional[date]
    service_name: Optional[str]
    service_category: Optional[str]
    official_amount: Optional[float]
    unit: Optional[str]
    source: Optional[str]
    active: Optional[bool]


class VetTariffRead(VetTariffBase):
    id: int
    last_updated_at: Optional[str]
    source_document_id: Optional[int]

    class Config:
        orm_mode = True
