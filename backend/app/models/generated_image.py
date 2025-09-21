import uuid
import enum
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from app.db.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class ViewEnum(str, enum.Enum):
    front = "front"
    side = "side"
    back = "back"
    three_quarters = "three_quarters"


class StatusEnum(str, enum.Enum):
    pending = "PENDING"
    ready = "READY"
    failed = "FAILED"


class TryOnRequest(Base):
    __tablename__ = "generated_images"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
        unique=True,
        index=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    mannequin_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("mannequins.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    garment_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("garments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    view: Mapped[ViewEnum] = mapped_column(
        Enum(ViewEnum, name="view_enum"),
        nullable=False,
    )

    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum, name="status_enum"),
        nullable=False,
        default=StatusEnum.pending,
    )

    image_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    generation_params: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
