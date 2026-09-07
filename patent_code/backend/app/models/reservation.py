from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.app.models.base import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    hotel_id = Column(Integer, ForeignKey("pet_hotels.id", ondelete="CASCADE"), nullable=False)
    pet_type = Column(String, nullable=False)
    pet_size = Column(String, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    guests = Column(Integer, nullable=False, default=1)
    total_price = Column(Float, nullable=True)
    status = Column(String, nullable=False, default="pending")
    pickup = Column(Boolean, default=False)
    pickup_fee = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    hotel = relationship("PetHotel")
