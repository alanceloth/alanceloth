from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import BaseSettings, Field, HttpUrl


class Settings(BaseSettings):
    app_name: str = Field(default="Cruise Price Monitor", validation_alias="APP_NAME")
    environment: Literal["development", "staging", "production"] = Field(
        default="development", validation_alias="APP_ENV"
    )
    database_url: str = Field(default="postgresql+psycopg2://postgres:postgres@localhost:5432/cruise_db", validation_alias="DATABASE_URL")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    scheduler_timezone: str = Field(default="UTC", validation_alias="SCHEDULER_TIMEZONE")
    price_alert_percentage: float = Field(
        default=10.0, validation_alias="PRICE_ALERT_PERCENTAGE"
    )

    alert_email_sender: str = Field(default="no-reply@example.com", validation_alias="ALERT_EMAIL_SENDER")
    alert_email_smtp: str = Field(default="smtp://localhost:1025", validation_alias="ALERT_EMAIL_SMTP")
    telegram_bot_token: str | None = Field(default=None, validation_alias="TELEGRAM_BOT_TOKEN")
    slack_webhook_url: HttpUrl | None = Field(default=None, validation_alias="SLACK_WEBHOOK_URL")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()
