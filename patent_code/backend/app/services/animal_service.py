def get_animal(db: Session, animal_id: int):
def list_animals_for_owner(db: Session, owner_id: int):
def update_animal(db: Session, animal: Animal, updates: dict):
def delete_animal(db: Session, animal: Animal):
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from backend.app.models.animal import Animal
from backend.app.schemas.animal import AnimalCreate, AnimalUpdate


async def create_animal(db: AsyncSession, owner_id: int, payload: AnimalCreate) -> Animal:
    a = Animal(
        owner_id=owner_id,
        name=payload.name,
        species=payload.species,
        breed=payload.breed,
        gender=payload.gender,
        birth_date=payload.birth_date,
        age=payload.age,
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


async def get_animal(db: AsyncSession, animal_id: int) -> Optional[Animal]:
    r = await db.execute(select(Animal).where(Animal.id == animal_id))
    return r.scalars().first()


async def list_animals_for_owner(db: AsyncSession, owner_id: int) -> List[Animal]:
    r = await db.execute(select(Animal).where(Animal.owner_id == owner_id))
    return r.scalars().all()


async def update_animal(db: AsyncSession, animal_id: int, updates: AnimalUpdate) -> Optional[Animal]:
    stmt = update(Animal).where(Animal.id == animal_id).values(**{k: v for k, v in updates.dict(exclude_unset=True).items()})
    await db.execute(stmt)
    await db.commit()
    return await get_animal(db, animal_id)


async def delete_animal(db: AsyncSession, animal_id: int) -> None:
    await db.execute(delete(Animal).where(Animal.id == animal_id))
    await db.commit()
