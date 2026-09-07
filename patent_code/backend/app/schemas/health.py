from pydantic import BaseModel
from typing import Optional
from datetime import date


class VaccinationCreate(BaseModel):
    name: str
    date: date
    next_date: Optional[date]
    vet_id: Optional[int]
    clinic: Optional[str]
    notes: Optional[str]


class MedicationCreate(BaseModel):
    name: str
    dose: Optional[str]
    frequency: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    notes: Optional[str]


class VisitCreate(BaseModel):
    vet_id: Optional[int]
    reason: Optional[str]
    notes: Optional[str]


class HealthDocumentCreate(BaseModel):
    filename: str
    content_type: str
    store_in_db: bool = False
