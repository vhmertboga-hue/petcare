from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from backend.app.db.session import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    animal_id = Column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=True)
    clinic_id = Column(Integer, ForeignKey("vets.id", ondelete="CASCADE"), nullable=True)
    tariff_id = Column(Integer, ForeignKey("vet_tariffs.id", ondelete="CASCADE"), nullable=True)
    lost_pet_id = Column(Integer, ForeignKey("lost_pets.id", ondelete="CASCADE"), nullable=True)
    adoption_id = Column(Integer, ForeignKey("adoptions.id", ondelete="CASCADE"), nullable=True)
    pet_hotel_id = Column(Integer, ForeignKey("pet_hotels.id", ondelete="CASCADE"), nullable=True)
    filename = Column(String, nullable=False)
    file_data = Column(LargeBinary, nullable=True)
    s3_key = Column(String, nullable=True)
    url = Column(String, nullable=True)
    mimetype = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User")
    animal = relationship("Animal", back_populates="photos")
    clinic = relationship("Vet")
    tariff = relationship("VetTariff")
    lost_pet = relationship("LostPet")
    adoption = relationship("Adoption")
    pet_hotel = relationship("PetHotel")
