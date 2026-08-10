from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.reconciliation.temporal_reconciliation import TemporalChange, TemporalStatus


@dataclass(frozen=True)
class ReconciliationSummary:
    total_compared: int
    additions: int
    removals: int
    persistence: int
    modifications: int

    @property
    def changed_or_new(self) -> int:
        return self.additions + self.modifications

    @property
    def match_rate(self) -> float:
        return self.persistence / self.total_compared if self.total_compared else 0.0

    @property
    def change_rate(self) -> float:
        return self.modifications / self.total_compared if self.total_compared else 0.0

    @property
    def addition_rate(self) -> float:
        return self.additions / self.total_compared if self.total_compared else 0.0

    @property
    def removal_rate(self) -> float:
        return self.removals / self.total_compared if self.total_compared else 0.0


def summarize_reconciliation(changes: Iterable[TemporalChange]) -> ReconciliationSummary:
    counts = {status: 0 for status in TemporalStatus}
    total = 0
    for change in changes:
        counts[change.status] += 1
        total += 1
    return ReconciliationSummary(
        total_compared=total,
        additions=counts[TemporalStatus.ADDITION],
        removals=counts[TemporalStatus.REMOVAL],
        persistence=counts[TemporalStatus.PERSISTENCE],
        modifications=counts[TemporalStatus.MODIFICATION],
    )
