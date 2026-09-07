from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.models.base import Base


class LostPet(Base):
    __tablename__ = "lost_pets"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name = Column(String, nullable=True)
    species = Column(String, nullable=False, index=True)
    breed = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    age = Column(String, nullable=True)
    color = Column(String, nullable=True)
    distinguishing_features = Column(Text, nullable=True)
    missing_date = Column(DateTime(timezone=True), nullable=True)
    missing_region = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    contact_method = Column(String, nullable=True)
    is_published = Column(Boolean, default=False)
    is_found = Column(Boolean, default=False)
    is_closed = Column(Boolean, default=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    show_exact_location = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User")
