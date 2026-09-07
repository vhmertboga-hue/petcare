from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel


class VaccinationCreate(BaseModel):
    name: str
    date: date
    next_date: Optional[date]
    veterinarian_id: Optional[int]
    clinic: Optional[str]
    note: Optional[str]


class VaccinationRead(VaccinationCreate):
    id: int

    class Config:
        orm_mode = True


class MedicationCreate(BaseModel):
    name: str
    dose: Optional[str]
    frequency: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    note: Optional[str]


class MedicationRead(MedicationCreate):
    id: int

    class Config:
        orm_mode = True


class VetVisitCreate(BaseModel):
    date: datetime
    veterinarian_id: Optional[int]
    clinic: Optional[str]
    reason: Optional[str]
    note: Optional[str]


class VetVisitRead(VetVisitCreate):
    id: int

    class Config:
        orm_mode = True


class LabTestCreate(BaseModel):
    name: str
    date: datetime
    result: Optional[str]
    note: Optional[str]


class LabTestRead(LabTestCreate):
    id: int

    class Config:
        orm_mode = True


class OperationCreate(BaseModel):
    name: str
    date: datetime
    note: Optional[str]


class OperationRead(OperationCreate):
    id: int

    class Config:
        orm_mode = True


class DiseaseHistoryCreate(BaseModel):
    name: str
    start_date: Optional[date]
    end_date: Optional[date]
    note: Optional[str]


class DiseaseHistoryRead(DiseaseHistoryCreate):
    id: int

    class Config:
        orm_mode = True


class WeightHistoryCreate(BaseModel):
    date: datetime
    weight: float


class WeightHistoryRead(WeightHistoryCreate):
    id: int

    class Config:
        orm_mode = True


class HealthNoteCreate(BaseModel):
    note: str


class HealthNoteRead(HealthNoteCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class HealthDocumentCreate(BaseModel):
    filename: str
    content_type: Optional[str]
    file_data: Optional[bytes]
    description: Optional[str]


class HealthDocumentRead(BaseModel):
    id: int
    filename: str
    content_type: Optional[str]
    uploaded_at: datetime

    class Config:
        orm_mode = True
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
