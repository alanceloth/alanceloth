from __future__ import annotations

from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from src.core.config import get_settings
from src.core.logging import get_logger
from src.scrapers.base import DummyScraper
from src.scrapers.runner import execute_scrapers
from src.core.metrics import scrape_counter, scrape_failures

logger = get_logger(__name__)
settings = get_settings()

scheduler = BlockingScheduler(timezone=settings.scheduler_timezone)


def scrape_job() -> None:
    logger.info("Starting scheduled scraping", timestamp=datetime.utcnow().isoformat())
    scrape_counter.inc()
    try:
        execute_scrapers([DummyScraper()])
    except Exception:
        scrape_failures.inc()
        logger.exception("Scraping job failed")
        raise


@scheduler.scheduled_job("cron", hour=3, minute=0)
def scheduled_scrape():
    scrape_job()


def start_scheduler() -> None:
    logger.info("Scheduler started", timezone=settings.scheduler_timezone)
    scheduler.start()


if __name__ == "__main__":
    start_scheduler()
