from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.reconciliation.summary import ReconciliationSummary


@dataclass(frozen=True)
class PeriodReconciliation:
    period: str
    summary: ReconciliationSummary


@dataclass(frozen=True)
class HistoricalSeries:
    periods: tuple[PeriodReconciliation, ...]

    @property
    def total_periods(self) -> int:
        return len(self.periods)


def build_historical_series(items: Iterable[PeriodReconciliation]) -> HistoricalSeries:
    """Return an ordered, immutable series for reporting purposes."""
    return HistoricalSeries(tuple(items))
