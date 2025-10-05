from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field, HttpUrl


class SourceBase(BaseModel):
    name: str
    website: HttpUrl | None = None


class SourceRead(SourceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CruiseData(BaseModel):
    source: SourceBase
    company: str
    ship: str | None = None
    origin: str
    destination: str
    departure_date: date
    duration_nights: int
    price: float
    currency: str = Field(default="USD", max_length=3)


class CruiseRead(BaseModel):
    id: int
    source_id: int
    company: str
    ship: str | None
    origin: str
    destination: str
    departure_date: date
    duration_nights: int
    price: float
    currency: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PriceHistoryRead(BaseModel):
    id: int
    cruise_id: int
    price: float
    currency: str
    recorded_at: datetime

    class Config:
        orm_mode = True


class AlertCreate(BaseModel):
    email: str | None = Field(default=None)
    telegram_chat_id: str | None = Field(default=None)
    slack_channel: str | None = Field(default=None)
    min_price: float | None = None
    max_price: float | None = None
    destinations: list[str] | None = None
    companies: list[str] | None = None
    percentage_drop: float | None = None


class AlertRead(AlertCreate):
    id: int


class RankingFilters(BaseModel):
    sort_by: str = Field(default="price", pattern="^(price|price_per_night|duration|company|destination)$")
    destination: str | None = None
    company: str | None = None
    duration_min: int | None = None
    duration_max: int | None = None


class WebhookPayload(BaseModel):
    event: str
    data: dict
