from pydantic import BaseModel
from typing import Optional, List
from app.models.user import GenderEnum

class MannequinMatch(BaseModel):
    """Request per trobar maniquí més semblant"""
    gender: GenderEnum
    height: float
    chest: float
    waist: float
    hips: float
    shoulders: Optional[float] = None

class BaseMannequinResponse(BaseModel):
    id: int
    name: str
    image_path: str
    gender: GenderEnum
    height: float
    chest: float
    waist: float
    hips: float
    shoulders: float
    similarity_score: Optional[float] = None
    
    class Config:
        from_attributes = True

class MannequinCustomize(BaseModel):
    """Request per customitzar maniquí"""
    base_mannequin_id: Optional[int] = None
    height: float
    chest: float
    waist: float
    hips: float
    shoulders: float

class UserMannequinResponse(BaseModel):
    id: int
    user_id: int
    base_mannequin_id: Optional[int] = None
    height: float
    chest: float
    waist: float
    hips: float
    shoulders: float
    image_path: Optional[str] = None
    is_custom: int
    
    class Config:
        from_attributes = True

class MannequinMatchResponse(BaseModel):
    matches: List[BaseMannequinResponse]
    best_match: BaseMannequinResponse