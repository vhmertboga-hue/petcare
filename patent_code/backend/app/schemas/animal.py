from typing import Optional, Dict
from datetime import date
from pydantic import BaseModel, Field


class AnimalCreate(BaseModel):
    name: str
    species: str = Field(default="Dog")
    breed: Optional[str]
    gender: Optional[str]
    birth_date: Optional[date]
    age: Optional[int]
    weight: Optional[float]
    height: Optional[float]
    color: Optional[str]
    microchip: Optional[str]
    neutered: Optional[bool] = False
    latitude: Optional[float]
    longitude: Optional[float]
    allergies: Optional[str]
    chronic_conditions: Optional[str]
    medications: Optional[str]
    vet_id: Optional[int]
    notes: Optional[str]


class AnimalRead(BaseModel):
    id: int
    owner_id: int
    name: str
    species: str
    breed: Optional[str]
    gender: Optional[str]
    birth_date: Optional[date]
    age: Optional[int]
    weight: Optional[float]
    height: Optional[float]
    color: Optional[str]
    neutered: bool
    latitude: Optional[float]
    longitude: Optional[float]
    allergies: Optional[str]
    chronic_conditions: Optional[str]
    medications: Optional[str]
    vet_id: Optional[int]
    notes: Optional[str]

    class Config:
        orm_mode = True


class AnimalPrivateRead(AnimalRead):
    microchip: Optional[str]


class AnimalUpdate(BaseModel):
    name: Optional[str]
    breed: Optional[str]
    gender: Optional[str]
    birth_date: Optional[date]
    age: Optional[int]
    weight: Optional[float]
    height: Optional[float]
    color: Optional[str]
    neutered: Optional[bool]
    latitude: Optional[float]
    longitude: Optional[float]
    allergies: Optional[str]
    chronic_conditions: Optional[str]
    medications: Optional[str]
    vet_id: Optional[int]
    notes: Optional[str]
