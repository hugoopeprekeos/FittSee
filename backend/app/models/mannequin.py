import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, Numeric, CheckConstraint, Enum
from app.db.database import Base
import enum


def generate_uuid() -> str:
    return str(uuid.uuid4())


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"


class Mannequin(Base):
    __tablename__ = "mannequins"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
        unique=True,
        index=True
    )

    gender: Mapped[GenderEnum] = mapped_column(
        Enum(GenderEnum, name="gender_enum"),
        nullable=False
    )

    # Mesures obligatòries (cm)
    total_height: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    chest_circumference: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    waist_circumference: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)

    # Mesures opcionals (cm)
    shoulder_width: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    hip_circumference: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    arm_length: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    inseam: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    back_length: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    users = relationship("User", back_populates="mannequin", uselist=True)

    __table_args__ = (
        CheckConstraint("total_height > 0", name="check_total_height_positive"),
        CheckConstraint("chest_circumference > 0", name="check_chest_positive"),
        CheckConstraint("waist_circumference > 0", name="check_waist_positive"),
        CheckConstraint("shoulder_width IS NULL OR shoulder_width > 0", name="check_shoulder_positive"),
        CheckConstraint("hip_circumference IS NULL OR hip_circumference > 0", name="check_hip_positive"),
        CheckConstraint("arm_length IS NULL OR arm_length > 0", name="check_arm_positive"),
        CheckConstraint("inseam IS NULL OR inseam > 0", name="check_inseam_positive"),
        CheckConstraint("back_length IS NULL OR back_length > 0", name="check_back_positive"),
    )
