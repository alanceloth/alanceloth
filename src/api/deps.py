from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy.orm import Session

from src.database.session import SessionLocal


def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
