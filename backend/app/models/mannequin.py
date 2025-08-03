from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from .user import GenderEnum

class BaseMannequin(Base):
    __tablename__ = "base_mannequins"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image_path = Column(String, nullable=False)
    
    gender = Column(Enum(GenderEnum), nullable=False)
    height = Column(Float, nullable=False)
    chest = Column(Float, nullable=False)
    waist = Column(Float, nullable=False)
    hips = Column(Float, nullable=False)
    shoulders = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserMannequin(Base):
    __tablename__ = "user_mannequins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    base_mannequin_id = Column(Integer, ForeignKey("base_mannequins.id"), nullable=True)
    
    height = Column(Float, nullable=False)
    chest = Column(Float, nullable=False)
    waist = Column(Float, nullable=False)
    hips = Column(Float, nullable=False)
    shoulders = Column(Float, nullable=False)

    image_path = Column(String, nullable=True)
    is_custom = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="mannequins")
    base_mannequin = relationship("BaseMannequin")
    generated_images = relationship("GeneratedImage", back_populates="mannequin")
