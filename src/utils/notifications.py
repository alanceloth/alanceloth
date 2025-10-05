from __future__ import annotations

from src.core.config import get_settings
from src.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

def notify_email(recipient: str, subject: str, body: str) -> None:
    logger.info("Sending email notification", to=recipient, subject=subject)


def notify_telegram(chat_id: str, message: str) -> None:
    if not settings.telegram_bot_token:
        logger.warning("Telegram notifications disabled: missing bot token")
        return
    logger.info("Sending telegram notification", chat_id=chat_id)


def notify_slack(channel: str, message: str) -> None:
    if not settings.slack_webhook_url:
        logger.warning("Slack notifications disabled: missing webhook URL")
        return
    logger.info("Sending slack notification", channel=channel)
