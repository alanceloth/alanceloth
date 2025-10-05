from __future__ import annotations

from collections.abc import Iterable

from src.api.schemas import CruiseData
from src.core.logging import get_logger
from src.database.crud import upsert_cruise
from src.database.session import session_scope
from src.scrapers.base import BaseScraper
from src.core.metrics import cruise_records

logger = get_logger(__name__)

def execute_scrapers(scrapers: Iterable[BaseScraper]) -> int:
    total_records = 0
    with session_scope() as session:
        for scraper in scrapers:
            logger.info("Running scraper", source=scraper.source_name)
            for data in scraper.fetch():
                upsert_cruise(session, data)
                total_records += 1
    cruise_records.set(total_records)
    logger.info("Scraper execution finished", records=total_records)
    return total_records
