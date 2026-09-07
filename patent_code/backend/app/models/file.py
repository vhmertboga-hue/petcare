from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from backend.app.db.session import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    filename = Column(String, nullable=False)
    content = Column(LargeBinary, nullable=True)
    s3_key = Column(String, nullable=True)
    url = Column(String, nullable=True)
    mimetype = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User")
    animal = relationship("Animal", back_populates="photos")
