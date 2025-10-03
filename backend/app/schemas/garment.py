# app/schemas/garment.py
from typing import Optional
from pydantic import Field, BaseModel, ConfigDict
from .common import BaseSchema, TimestampMixin
from app.models.garment import FitEnum  

class GarmentCreate(BaseSchema):
    name: str = Field(min_length=1, max_length=255)
    fit: Optional[FitEnum] = None

    chest_circumference: Optional[float] = Field(default=None, gt=0)
    waist_circumference: Optional[float] = Field(default=None, gt=0)
    hip_circumference: Optional[float] = Field(default=None, gt=0)
    length: Optional[float] = Field(default=None, gt=0)
    shoulder_width: Optional[float] = Field(default=None, gt=0)
    sleeve_length: Optional[float] = Field(default=None, gt=0)


class GarmentUpdate(BaseSchema):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    fit: Optional[FitEnum] = None

    chest_circumference: Optional[float] = Field(default=None, gt=0)
    waist_circumference: Optional[float] = Field(default=None, gt=0)
    hip_circumference: Optional[float] = Field(default=None, gt=0)
    length: Optional[float] = Field(default=None, gt=0)
    shoulder_width: Optional[float] = Field(default=None, gt=0)
    sleeve_length: Optional[float] = Field(default=None, gt=0)


class GarmentPublic(TimestampMixin):
    id: str
    name: str
    fit: Optional[FitEnum] = None

    chest_circumference: Optional[float] = None
    waist_circumference: Optional[float] = None
    hip_circumference: Optional[float] = None
    length: Optional[float] = None
    shoulder_width: Optional[float] = None
    sleeve_length: Optional[float] = None


class GarmentInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    fit: Optional[FitEnum] = None

    chest_circumference: Optional[float] = None
    waist_circumference: Optional[float] = None
    hip_circumference: Optional[float] = None
    length: Optional[float] = None
    shoulder_width: Optional[float] = None
    sleeve_length: Optional[float] = None
