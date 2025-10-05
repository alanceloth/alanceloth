from __future__ import annotations

from datetime import datetime, date

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    cruises: Mapped[list["Cruise"]] = relationship("Cruise", back_populates="source", cascade="all, delete-orphan")


class Cruise(Base):
    __tablename__ = "cruises"
    __table_args__ = (UniqueConstraint("source_id", "ship", "departure_date", name="uq_cruise_source_ship_departure"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    company: Mapped[str] = mapped_column(String(120), nullable=False)
    ship: Mapped[str | None] = mapped_column(String(120), nullable=True)
    origin: Mapped[str] = mapped_column(String(120), nullable=False)
    destination: Mapped[str] = mapped_column(String(120), nullable=False)
    departure_date: Mapped[date] = mapped_column(Date, nullable=False)
    duration_nights: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    source: Mapped[Source] = relationship("Source", back_populates="cruises")
    price_history: Mapped[list["PriceHistory"]] = relationship(
        "PriceHistory", back_populates="cruise", cascade="all, delete-orphan"
    )


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cruise_id: Mapped[int] = mapped_column(ForeignKey("cruises.id", ondelete="CASCADE"), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    cruise: Mapped[Cruise] = relationship("Cruise", back_populates="price_history")
