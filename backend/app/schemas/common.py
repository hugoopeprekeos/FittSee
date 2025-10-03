from datetime import datetime
from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="ignore",
    )

class IDSchema(BaseSchema):
    id: str

class TimestampMixin(BaseSchema):
    created_at: datetime | None = None
    updated_at: datetime | None = None
