from pydantic import EmailStr, Field, ConfigDict, BaseModel
from .common import BaseSchema, IDSchema, TimestampMixin

class UserCreate(BaseSchema):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None

class UserUpdate(BaseSchema):
    full_name: str | None = None


class UserPublic(IDSchema, TimestampMixin):
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: EmailStr
    hashed_password: str
    full_name: str | None = None
