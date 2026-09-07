from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.models.base import Base


class Adoption(Base):
    __tablename__ = "adoptions"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    age = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    color = Column(String, nullable=True)
    sterilized = Column(Boolean, nullable=True)
    vaccinated = Column(Boolean, nullable=True)
    location_region = Column(String, nullable=True)
    contact_method = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, approved, rejected, suspended, completed
    is_closed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User")
