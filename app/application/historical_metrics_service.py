from __future__ import annotations

from dataclasses import dataclass
from app.domain.query_filters import HistoricalQueryFilters
from app.infrastructure.historical_repository import HistoricalRepository


@dataclass(frozen=True)
class MetricGroup:
    dimension: str
    value: str
    count: int


@dataclass(frozen=True)
class HistoricalMetrics:
    total: int
    by_period: list[MetricGroup]
    by_campaign: list[MetricGroup]
    by_version: list[MetricGroup]
    by_channel: list[MetricGroup]
    by_state: list[MetricGroup]
    by_key: list[MetricGroup]
    by_batch: list[MetricGroup]
    duplicates: int


class HistoricalMetricsService:
    def __init__(self, repository: HistoricalRepository) -> None:
        self.repository = repository

    def summarize(self, filters: HistoricalQueryFilters | None = None) -> HistoricalMetrics:
        return self.repository.metrics(filters or HistoricalQueryFilters())
