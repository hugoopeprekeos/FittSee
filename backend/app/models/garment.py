import uuid
import enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func, Numeric, Enum
from app.db.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class FitEnum(str, enum.Enum):
    regular = "regular"
    classic = "classic"
    slim = "slim"
    athletic = "athletic"
    relaxed = "relaxed"
    oversized = "oversized"
    missy = "missy"
    cropped = "cropped"


class Garment(Base):
    __tablename__ = "garments"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
        unique=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    fit: Mapped[FitEnum | None] = mapped_column(
        Enum(FitEnum, name="fit_enum"),
        nullable=True
    )

    chest_circumference: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    waist_circumference: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    hip_circumference: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    length: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    shoulder_width: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    sleeve_length: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
