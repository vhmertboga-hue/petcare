from sqlalchemy import Column, Integer, String, Float, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from backend.app.models.base import Base


class Vet(Base):
    __tablename__ = "vets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    clinic = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    working_hours = Column(JSON, nullable=True)  # structured hours per weekday
    emergency = Column(Boolean, default=False)
    open_24_7 = Column(Boolean, default=False)
    services = Column(Text, nullable=True)
    is_open = Column(Boolean, default=True)
    rating = Column(Float, nullable=True)

    photos = relationship("File")

