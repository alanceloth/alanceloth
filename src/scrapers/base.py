from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from src.api.schemas import CruiseData


class BaseScraper(ABC):
    source_name: str

    @abstractmethod
    def fetch(self) -> Iterable[CruiseData]:
        """Fetch cruise data from source."""


class DummyScraper(BaseScraper):
    source_name = "Dummy"

    def fetch(self) -> Iterable[CruiseData]:
        return []
