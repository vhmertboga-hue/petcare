from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.animal import Animal
from backend.app.schemas.animal import AnimalCreate


async def create_animal(db: AsyncSession, owner_id: int, payload: AnimalCreate) -> Animal:
    a = Animal(
        owner_id=owner_id,
        name=payload.name,
        species=payload.species,
        breed=payload.breed,
        gender=payload.gender,
        birth_date=payload.birth_date,
        weight=payload.weight,
        height=payload.height,
        color=payload.color,
        microchip=payload.microchip,
        neutered=payload.neutered,
        latitude=payload.latitude,
        longitude=payload.longitude,
        allergies=payload.allergies,
        chronic_conditions=payload.chronic_conditions,
        medications=payload.medications,
        vet_id=payload.vet_id,
        notes=payload.notes,
    )
    db.add(a)
    await db.flush()
    await db.commit()
    await db.refresh(a)
    return a


async def get_animal(db: AsyncSession, animal_id: int):
    from sqlalchemy import select

    r = await db.execute(select(Animal).where(Animal.id == animal_id))
    return r.scalars().first()
from backend.app.db.session import SessionLocal
from backend.app.models.animal import Animal
from sqlalchemy.orm import Session


def create_animal(db: Session, owner_id: int, data: dict):
    a = Animal(owner_id=owner_id, **data)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def get_animal(db: Session, animal_id: int):
    return db.query(Animal).filter(Animal.id == animal_id).first()


def list_animals_for_owner(db: Session, owner_id: int):
    return db.query(Animal).filter(Animal.owner_id == owner_id).all()


def update_animal(db: Session, animal: Animal, updates: dict):
    for k, v in updates.items():
        setattr(animal, k, v)
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal


def delete_animal(db: Session, animal: Animal):
    db.delete(animal)
    db.commit()
