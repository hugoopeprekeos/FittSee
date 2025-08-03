from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class GeneratedImage(Base):
    __tablename__ = "generated_images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mannequin_id = Column(Integer, ForeignKey("user_mannequins.id"), nullable=False)
    garment_id = Column(Integer, ForeignKey("garments.id"), nullable=True)

    image_path = Column(String, nullable=False)
    prompt_used = Column(String, nullable=True)
    generation_params = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="generated_images")
    mannequin = relationship("UserMannequin", back_populates="generated_images")
    garment = relationship("Garment")
