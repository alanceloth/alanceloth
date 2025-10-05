from __future__ import annotations

from fastapi import APIRouter

from src.api.schemas import WebhookPayload
from src.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("")
def receive_webhook(payload: WebhookPayload) -> dict[str, str]:
    logger.info("Webhook received", event=payload.event, data=payload.data)
    return {"status": "accepted"}
