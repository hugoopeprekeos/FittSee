from pydantic import BaseModel
from typing import Optional
from app.models.garment import GarmentTypeEnum, FitTypeEnum, SizeEnum

class GarmentCreate(BaseModel):
    name: str
    type: GarmentTypeEnum
    brand: Optional[str] = None
    color: str
    size: SizeEnum
    fit: FitTypeEnum
    chest_fit: Optional[float] = None
    waist_fit: Optional[float] = None
    hip_fit: Optional[float] = None
    length: Optional[float] = None
    reference_image: Optional[str] = None

class GarmentResponse(BaseModel):
    id: int
    name: str
    type: GarmentTypeEnum
    brand: Optional[str] = None
    color: str
    size: SizeEnum
    fit: FitTypeEnum
    chest_fit: Optional[float] = None
    waist_fit: Optional[float] = None
    hip_fit: Optional[float] = None
    length: Optional[float] = None
    reference_image: Optional[str] = None
    
    class Config:
        from_attributes = True

class TryOnRequest(BaseModel):
    """Request per provar una peça de roba"""
    mannequin_id: int
    garment_id: int
    additional_prompt: Optional[str] = None

class GeneratedImageResponse(BaseModel):
    id: int
    user_id: int
    mannequin_id: int
    garment_id: Optional[int] = None
    image_path: str
    prompt_used: Optional[str] = None
    
    class Config:
        from_attributes = True