from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class HistoricalQueryFilters:
    date_from: date | None = None
    date_to: date | None = None
    estado: str | None = None
    campana: str | None = None
    version: str | None = None
    clave: str | None = None
    canal_base: str | None = None
    batch_id: str | None = None
    source_filename: str | None = None
    limit: int = 100
    offset: int = 0
    sort_by: str = "fecha"
    descending: bool = False

    def __post_init__(self) -> None:
        if self.limit < 1 or self.limit > 5000:
            raise ValueError("limit debe estar entre 1 y 5000")
        if self.offset < 0:
            raise ValueError("offset no puede ser negativo")
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise ValueError("date_from no puede ser posterior a date_to")
