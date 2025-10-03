from pydantic import Field, BaseModel, ConfigDict
from .common import BaseSchema, IDSchema, TimestampMixin

class UserMannequinCreate(BaseSchema):
    # Obligatòries (cm)
    total_height: float = Field(gt=0)
    chest_circumference: float = Field(gt=0)
    waist_circumference: float = Field(gt=0)
    # Opcionals (cm)
    shoulder_width: float | None = Field(default=None, gt=0)
    hip_circumference: float | None = Field(default=None, gt=0)
    arm_length: float | None = Field(default=None, gt=0)
    inseam: float | None = Field(default=None, gt=0)
    back_length: float | None = Field(default=None, gt=0)

class UserMannequinUpdate(BaseSchema):
    # Tot opcional per permetre actualitzacions parcials
    total_height: float | None = Field(default=None, gt=0)
    chest_circumference: float | None = Field(default=None, gt=0)
    waist_circumference: float | None = Field(default=None, gt=0)
    shoulder_width: float | None = Field(default=None, gt=0)
    hip_circumference: float | None = Field(default=None, gt=0)
    arm_length: float | None = Field(default=None, gt=0)
    inseam: float | None = Field(default=None, gt=0)
    back_length: float | None = Field(default=None, gt=0)


class UserMannequinPublic(IDSchema, TimestampMixin):
    total_height: float
    chest_circumference: float
    waist_circumference: float
    shoulder_width: float | None = None
    hip_circumference: float | None = None
    arm_length: float | None = None
    inseam: float | None = None
    back_length: float | None = None


class UserMannequinInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    total_height: float
    chest_circumference: float
    waist_circumference: float
    shoulder_width: float | None = None
    hip_circumference: float | None = None
    arm_length: float | None = None
    inseam: float | None = None
    back_length: float | None = None
