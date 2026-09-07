from sqlalchemy import Column, Integer, String, Boolean, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from backend.app.db.session import Base


class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False, default="Dog")
    breed = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    color = Column(String, nullable=True)
    microchip = Column(String, nullable=True)
    neutered = Column(Boolean, default=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    allergies = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    vet_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)

    owner = relationship("User", foreign_keys=[owner_id])
    vet = relationship("User", foreign_keys=[vet_id])
    photos = relationship("File", back_populates="animal")
