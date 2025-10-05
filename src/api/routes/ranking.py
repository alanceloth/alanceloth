from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_session
from src.api.schemas import CruiseRead, RankingFilters
from src.database import crud

router = APIRouter(prefix="/rank", tags=["ranking"])


@router.get("", response_model=list[CruiseRead])
def rank_cruises(
    filters: RankingFilters = Depends(),
    session: Session = Depends(get_session),
) -> list[CruiseRead]:
    return crud.get_ranked_cruises(session, filters)
