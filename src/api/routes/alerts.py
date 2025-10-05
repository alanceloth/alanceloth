from __future__ import annotations

from fastapi import APIRouter

from src.api.schemas import AlertCreate, AlertRead
from src.utils.alerts import AlertManager

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("", response_model=AlertRead, status_code=201)
def create_alert(alert: AlertCreate) -> AlertRead:
    return AlertManager.create_alert(alert)


@router.get("", response_model=list[AlertRead])
def list_alerts() -> list[AlertRead]:
    return AlertManager.list_alerts()
