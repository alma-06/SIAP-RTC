from __future__ import annotations

from dataclasses import dataclass
from app.domain.query_filters import HistoricalQueryFilters
from app.infrastructure.historical_repository import HistoricalRepository


@dataclass(frozen=True)
class HistoricalQueryResult:
    records: list[dict[str, object]]
    total: int
    limit: int
    offset: int


class HistoricalQueryService:
    def __init__(self, repository: HistoricalRepository) -> None:
        self.repository = repository

    def search(self, filters: HistoricalQueryFilters) -> HistoricalQueryResult:
        records, total = self.repository.search(filters)
        return HistoricalQueryResult(
            records=records, total=total, limit=filters.limit, offset=filters.offset
        )
