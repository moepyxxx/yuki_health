from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Date, ForeignKey
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


class DailyFamilyFacesImage(Base):
    __tablename__ = "daily_family_faces_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    family_id: Mapped[int] = mapped_column(ForeignKey("families.id"))
    image_src: Mapped[str] = mapped_column(String, unique=True)
