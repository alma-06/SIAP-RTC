from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.dashboard.model import DashboardPeriod


@dataclass(frozen=True)
class ComparisonRow:
    period: str
    total_compared: int
    additions: int
    modifications: int
    persistence: int
    removals: int
    match_rate: float
    change_rate: float
    comparable: bool
    evidence_id: str


@dataclass(frozen=True)
class ExecutiveComparison:
    rows: tuple[ComparisonRow, ...]
    comparable: bool
    warnings: tuple[str, ...]


def build_executive_comparison(periods: Iterable[DashboardPeriod]) -> ExecutiveComparison:
    items = tuple(periods)
    warnings: list[str] = []
    for item in items:
        if not item.comparable:
            warnings.append(f"{item.period}: periodo no comparable")
    rows = tuple(
        ComparisonRow(
            period=item.period,
            total_compared=item.total_compared,
            additions=item.additions,
            modifications=item.modifications,
            persistence=item.persistence,
            removals=item.removals,
            match_rate=item.match_rate,
            change_rate=item.change_rate,
            comparable=item.comparable,
            evidence_id=item.evidence_id,
        )
        for item in items
    )
    return ExecutiveComparison(rows, not warnings, tuple(warnings))
