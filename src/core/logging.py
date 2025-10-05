from __future__ import annotations

import sys
from loguru import logger

from src.core.config import get_settings

settings = get_settings()

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    backtrace=True,
    diagnose=False,
    enqueue=True,
    level=settings.log_level,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
)


def get_logger(name: str):
    return logger.bind(name=name)
