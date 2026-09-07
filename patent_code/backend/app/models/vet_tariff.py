from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.models.base import Base


class VetTariff(Base):
    __tablename__ = "vet_tariffs"

    id = Column(Integer, primary_key=True, index=True)
    province = Column(String, nullable=False, index=True)
    chamber = Column(String, nullable=True)
    year = Column(Integer, nullable=False, index=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    service_name = Column(String, nullable=False, index=True)
    service_category = Column(String, nullable=True, index=True)
    official_amount = Column(Float, nullable=True)
    unit = Column(String, nullable=True)
    source = Column(String, nullable=True)
    source_document_id = Column(Integer, ForeignKey("files.id", ondelete="SET NULL"), nullable=True)
    last_updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    active = Column(Boolean, default=True)

    source_document = relationship("File")
