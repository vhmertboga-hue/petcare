from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.models.base import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=True, unique=True)
    type = Column(String, nullable=False)  # clinic, vet, hotel, daycare
    status = Column(String, nullable=False, default="pending")  # pending, verified, rejected, suspended
    description = Column(Text, nullable=True)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    phone = Column(String, nullable=True)
    logo_file_id = Column(Integer, ForeignKey("files.id", ondelete="SET NULL"), nullable=True)
    photos = Column(JSON, nullable=True)
    working_hours = Column(JSON, nullable=True)
    services = Column(JSON, nullable=True)
    prices = Column(JSON, nullable=True)
    commission_rate = Column(Float, nullable=True, default=0.0)
    revenue = Column(Float, nullable=True, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User")
    logo_file = relationship("File")
