from __future__ import annotations

from datetime import datetime

from sqlalchemy import and_, asc, desc, func, select
from sqlalchemy.orm import Session

from src.api.schemas import CruiseData, RankingFilters
from src.database import models


def get_cruises(session: Session) -> list[models.Cruise]:
    statement = select(models.Cruise)
    return list(session.scalars(statement))


def get_cruise(session: Session, cruise_id: int) -> models.Cruise | None:
    return session.get(models.Cruise, cruise_id)


def upsert_cruise(session: Session, cruise_data: CruiseData) -> models.Cruise:
    source = session.query(models.Source).filter_by(name=cruise_data.source.name).one_or_none()
    if not source:
        source = models.Source(
            name=cruise_data.source.name,
            website=str(cruise_data.source.website) if cruise_data.source.website else None,
        )
        session.add(source)
        session.flush()

    cruise = (
        session.query(models.Cruise)
        .filter(
            models.Cruise.source_id == source.id,
            models.Cruise.ship == cruise_data.ship,
            models.Cruise.departure_date == cruise_data.departure_date,
        )
        .one_or_none()
    )

    if cruise:
        cruise.company = cruise_data.company
        cruise.origin = cruise_data.origin
        cruise.destination = cruise_data.destination
        cruise.duration_nights = cruise_data.duration_nights
        cruise.price = cruise_data.price
        cruise.currency = cruise_data.currency
        cruise.updated_at = datetime.utcnow()
    else:
        cruise = models.Cruise(
            source=source,
            company=cruise_data.company,
            ship=cruise_data.ship,
            origin=cruise_data.origin,
            destination=cruise_data.destination,
            departure_date=cruise_data.departure_date,
            duration_nights=cruise_data.duration_nights,
            price=cruise_data.price,
            currency=cruise_data.currency,
        )
        session.add(cruise)
        session.flush()

    price_entry = models.PriceHistory(
        cruise_id=cruise.id,
        price=cruise_data.price,
        currency=cruise_data.currency,
    )
    session.add(price_entry)

    return cruise


def get_ranked_cruises(session: Session, filters: RankingFilters) -> list[models.Cruise]:
    statement = session.query(models.Cruise)

    if filters.destination:
        statement = statement.filter(models.Cruise.destination.ilike(f"%{filters.destination}%"))
    if filters.company:
        statement = statement.filter(models.Cruise.company.ilike(f"%{filters.company}%"))
    if filters.duration_min is not None:
        statement = statement.filter(models.Cruise.duration_nights >= filters.duration_min)
    if filters.duration_max is not None:
        statement = statement.filter(models.Cruise.duration_nights <= filters.duration_max)

    if filters.sort_by == "price":
        statement = statement.order_by(asc(models.Cruise.price))
    elif filters.sort_by == "price_per_night":
        statement = statement.order_by(asc(models.Cruise.price / func.nullif(models.Cruise.duration_nights, 0)))
    elif filters.sort_by == "duration":
        statement = statement.order_by(desc(models.Cruise.duration_nights))
    elif filters.sort_by == "company":
        statement = statement.order_by(asc(models.Cruise.company))
    elif filters.sort_by == "destination":
        statement = statement.order_by(asc(models.Cruise.destination))

    return statement.all()


def filter_price_drops(session: Session, percentage: float) -> list[models.Cruise]:
    subquery = (
        session.query(
            models.PriceHistory.cruise_id,
            func.max(models.PriceHistory.recorded_at).label("max_recorded_at"),
        )
        .group_by(models.PriceHistory.cruise_id)
        .subquery()
    )

    latest_prices = (
        session.query(models.PriceHistory)
        .join(
            subquery,
            and_(
                models.PriceHistory.cruise_id == subquery.c.cruise_id,
                models.PriceHistory.recorded_at == subquery.c.max_recorded_at,
            ),
        )
        .subquery()
    )

    previous_prices = (
        session.query(models.PriceHistory)
        .filter(models.PriceHistory.recorded_at < latest_prices.c.recorded_at)
        .subquery()
    )

    statement = (
        session.query(models.Cruise)
        .join(latest_prices, models.Cruise.id == latest_prices.c.cruise_id)
        .join(previous_prices, models.Cruise.id == previous_prices.c.cruise_id)
        .filter(
            (previous_prices.c.price - latest_prices.c.price) / previous_prices.c.price
            >= (percentage / 100.0)
        )
    )

    return statement.all()
