from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from loguru import logger

from src.api.schemas import AlertCreate, AlertRead


@dataclass
class AlertRecord:
    id: int
    data: AlertCreate


class AlertManager:
    _alerts: ClassVar[list[AlertRecord]] = []
    _counter: ClassVar[int] = 0

    @classmethod
    def create_alert(cls, payload: AlertCreate) -> AlertRead:
        cls._counter += 1
        record = AlertRecord(id=cls._counter, data=payload)
        cls._alerts.append(record)
        logger.info("Alert registered", alert_id=record.id)
        return AlertRead(id=record.id, **payload.model_dump())

    @classmethod
    def list_alerts(cls) -> list[AlertRead]:
        return [AlertRead(id=record.id, **record.data.model_dump()) for record in cls._alerts]
