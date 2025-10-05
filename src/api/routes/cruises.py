from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.deps import get_session
from src.api.schemas import CruiseRead
from src.database import crud

router = APIRouter(prefix="/cruises", tags=["cruises"])


@router.get("", response_model=list[CruiseRead])
def list_cruises(session: Session = Depends(get_session)) -> list[CruiseRead]:
    cruises = crud.get_cruises(session)
    return cruises


@router.get("/{cruise_id}", response_model=CruiseRead)
def get_cruise(cruise_id: int, session: Session = Depends(get_session)) -> CruiseRead:
    cruise = crud.get_cruise(session, cruise_id)
    if not cruise:
        raise HTTPException(status_code=404, detail="Cruise not found")
    return cruise
