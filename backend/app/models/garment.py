from sqlalchemy import Column, Integer, String, Float, Enum, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum

class GarmentTypeEnum(str, enum.Enum):
    tshirt = "tshirt"
    pants = "pants"
    dress = "dress"
    jacket = "jacket"
    skirt = "skirt"
    sweater = "sweater"

class FitTypeEnum(str, enum.Enum):
    slim = "slim"
    regular = "regular"
    loose = "loose"
    oversized = "oversized"

class SizeEnum(str, enum.Enum):
    xs = "XS"
    s = "S"
    m = "M"
    l = "L"
    xl = "XL"
    xxl = "XXL"

class Garment(Base):
    __tablename__ = "garments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(GarmentTypeEnum), nullable=False)
    brand = Column(String, nullable=True)
    color = Column(String, nullable=False)
    size = Column(Enum(SizeEnum), nullable=False)
    fit = Column(Enum(FitTypeEnum), nullable=False)
    
    # Mesures de la peça
    chest_fit = Column(Float, nullable=True)
    waist_fit = Column(Float, nullable=True)
    hip_fit = Column(Float, nullable=True)
    length = Column(Float, nullable=True)

    reference_image = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
