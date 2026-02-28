from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Date, ForeignKey, Boolean, Float
from datetime import date


class Base(DeclarativeBase):
    pass


class Family(Base):
    __tablename__ = "families"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    nickname: Mapped[str | None] = mapped_column(String, nullable=True)
    gender: Mapped[int] = mapped_column(Integer)
    birthday: Mapped[date] = mapped_column(Date)
    bird_type: Mapped[int] = mapped_column(Integer)


class DailyFamilyFecesImage(Base):
    __tablename__ = "daily_record_feces_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    family_id: Mapped[int | None] = mapped_column(
        ForeignKey("families.id", ondelete="SET NULL"), nullable=True
    )
    image_src: Mapped[str | None] = mapped_column(String, unique=True)
    color: Mapped[int | None] = mapped_column(Integer, nullable=True)
    has_urates: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    wateriness: Mapped[int | None] = mapped_column(Integer, nullable=True)
    has_undigested_seeds: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    impressions: Mapped[str | None] = mapped_column(String, nullable=True)
