from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.models.health import (
    Vaccination,
    Medication,
    VetVisit,
    LabTest,
    Operation,
    DiseaseHistory,
    WeightHistory,
    HealthNote,
    HealthDocument,
)
from backend.app.schemas.health import (
    VaccinationCreate,
    MedicationCreate,
    VetVisitCreate,
    LabTestCreate,
    OperationCreate,
    DiseaseHistoryCreate,
    WeightHistoryCreate,
    HealthNoteCreate,
    HealthDocumentCreate,
)


async def create_vaccination(db: AsyncSession, animal_id: int, payload: VaccinationCreate) -> Vaccination:
    v = Vaccination(
        animal_id=animal_id,
        name=payload.name,
        date=payload.date,
        next_date=payload.next_date,
        veterinarian_id=payload.veterinarian_id,
        clinic=payload.clinic,
        note=payload.note,
    )
    db.add(v)
    await db.flush()
    await db.commit()
    await db.refresh(v)
    return v


async def list_vaccinations(db: AsyncSession, animal_id: int) -> List[Vaccination]:
    r = await db.execute(select(Vaccination).where(Vaccination.animal_id == animal_id))
    return r.scalars().all()


async def create_medication(db: AsyncSession, animal_id: int, payload: MedicationCreate) -> Medication:
    m = Medication(
        animal_id=animal_id,
        name=payload.name,
        dose=payload.dose,
        frequency=payload.frequency,
        start_date=payload.start_date,
        end_date=payload.end_date,
        note=payload.note,
    )
    db.add(m)
    await db.flush()
    await db.commit()
    await db.refresh(m)
    return m


async def list_medications(db: AsyncSession, animal_id: int) -> List[Medication]:
    r = await db.execute(select(Medication).where(Medication.animal_id == animal_id))
    return r.scalars().all()
from backend.app.db.session import SessionLocal
from backend.app.models.health import Vaccination, Medication, Visit, HealthDocument, WeightHistory, HealthNote
from sqlalchemy.orm import Session
from datetime import datetime
import os


def add_vaccination(db: Session, animal_id: int, data: dict):
    v = Vaccination(animal_id=animal_id, **data)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


def add_medication(db: Session, animal_id: int, data: dict):
    m = Medication(animal_id=animal_id, **data)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


def add_visit(db: Session, animal_id: int, data: dict):
    v = Visit(animal_id=animal_id, **data)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


def add_health_note(db: Session, animal_id: int, note: str):
    n = HealthNote(animal_id=animal_id, note=note)
    db.add(n)
    db.commit()
    db.refresh(n)
    return n


def save_document(db: Session, animal_id: int, filename: str, content_type: str, data: bytes, store_in_db: bool = False, storage_dir: str = "storage"):
    # save file to FS
    os.makedirs(storage_dir, exist_ok=True)
    path = os.path.join(storage_dir, filename)
    with open(path, "wb") as f:
        f.write(data)

    doc = HealthDocument(animal_id=animal_id, filename=filename, content_type=content_type, file_path=path)
    if store_in_db:
        doc.file_data = data
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc
