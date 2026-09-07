from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.models.base import Base


class UserLocation(Base):
    __tablename__ = "user_locations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    opt_in = Column(Boolean, default=True)  # whether user agrees receiving nearby alerts
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
