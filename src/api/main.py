from __future__ import annotations

from fastapi import FastAPI

from src.api.routes import alerts, cruises, ranking, webhook, metrics
from src.core.config import get_settings
from src.core.logging import logger

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.include_router(cruises.router)
app.include_router(ranking.router)
app.include_router(alerts.router)
app.include_router(webhook.router)
app.include_router(metrics.router)


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    logger.info("Health check invoked")
    return {"status": "ok"}
