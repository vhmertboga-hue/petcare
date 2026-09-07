from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship

from backend.app.db.session import Base


class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    next_date = Column(Date, nullable=True)
    veterinarian_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    clinic = Column(String, nullable=True)
    note = Column(Text, nullable=True)

    animal = relationship("Animal")


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    dose = Column(String, nullable=True)
    frequency = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    note = Column(Text, nullable=True)

    animal = relationship("Animal")


class VetVisit(Base):
    __tablename__ = "vet_visits"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    date = Column(DateTime, nullable=False)
    veterinarian_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    clinic = Column(String, nullable=True)
    reason = Column(Text, nullable=True)
    note = Column(Text, nullable=True)

    animal = relationship("Animal")


class LabTest(Base):
    __tablename__ = "lab_tests"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    result = Column(Text, nullable=True)
    note = Column(Text, nullable=True)

    animal = relationship("Animal")


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    note = Column(Text, nullable=True)

    animal = relationship("Animal")


class DiseaseHistory(Base):
    __tablename__ = "disease_histories"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    note = Column(Text, nullable=True)

    animal = relationship("Animal")


class WeightHistory(Base):
    __tablename__ = "weight_histories"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    date = Column(DateTime, nullable=False)
    weight = Column(Float, nullable=False)

    animal = relationship("Animal")


class HealthDocument(Base):
    __tablename__ = "health_documents"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    file_id = Column(Integer, ForeignKey("files.id", ondelete="SET NULL"), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    animal = relationship("Animal")
from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey, Text, LargeBinary
from sqlalchemy.sql import func
from backend.app.models.base import Base


class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    next_date = Column(Date, nullable=True)
    vet_id = Column(Integer, ForeignKey("vets.id", ondelete="SET NULL"), nullable=True)
    clinic = Column(String, nullable=True)
    notes = Column(Text, nullable=True)


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    dose = Column(String, nullable=True)
    frequency = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    vet_id = Column(Integer, ForeignKey("vets.id", ondelete="SET NULL"), nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)


class LabTest(Base):
    __tablename__ = "lab_tests"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=True)
    result = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)


class Illness(Base):
    __tablename__ = "illnesses"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)


class WeightHistory(Base):
    __tablename__ = "weight_history"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    weight = Column(Float, nullable=False)


class HealthNote(Base):
    __tablename__ = "health_notes"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    note = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HealthDocument(Base):
    __tablename__ = "health_documents"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=True)
    file_data = Column(LargeBinary, nullable=True)  # optional DB storage
    file_path = Column(String, nullable=True)  # optional FS/S3 path
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
