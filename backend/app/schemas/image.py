# app/schemas/image.py
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from .common import BaseSchema, TimestampMixin
from app.models.generated_image import ViewEnum, StatusEnum

class TryOnCreate(BaseSchema):
    mannequin_id: str = Field(min_length=1)
    garment_id: str = Field(min_length=1)
    view: ViewEnum

class TryOnPublic(TimestampMixin):
    id: str
    user_id: str
    mannequin_id: Optional[str] = None
    garment_id: Optional[str] = None
    view: ViewEnum
    status: StatusEnum
    image_url: Optional[str] = None
    generation_params: Optional[Dict[str, Any]] = None

class TryOnInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    mannequin_id: Optional[str] = None
    garment_id: Optional[str] = None
    view: ViewEnum
    status: StatusEnum
    image_url: Optional[str] = None
    generation_params: Optional[Dict[str, Any]] = None
    created_at: datetime
