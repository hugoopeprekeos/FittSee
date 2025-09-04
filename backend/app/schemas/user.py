from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import GenderEnum

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserMeasurements(BaseModel):
    gender: GenderEnum
    height: float
    chest: float
    waist: float
    hips: float
    shoulders: Optional[float] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    gender: Optional[GenderEnum] = None
    height: Optional[float] = None
    chest: Optional[float] = None
    waist: Optional[float] = None
    hips: Optional[float] = None
    shoulders: Optional[float] = None

class UserResponse(BaseModel):
    id: int
    email: str
    gender: Optional[GenderEnum] = None
    height: Optional[float] = None
    chest: Optional[float] = None
    waist: Optional[float] = None
    hips: Optional[float] = None
    shoulders: Optional[float] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None