from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.dashboard.model import DashboardPeriod


@dataclass(frozen=True)
class TrendPoint:
    period: str
    additions: int
    modifications: int
    persistence: int
    removals: int


@dataclass(frozen=True)
class QualityPoint:
    period: str
    match_rate: float
    change_rate: float


def build_trend_points(periods: Iterable[DashboardPeriod]) -> tuple[TrendPoint, ...]:
    return tuple(
        TrendPoint(
            period=item.period,
            additions=item.additions,
            modifications=item.modifications,
            persistence=item.persistence,
            removals=item.removals,
        )
        for item in periods
    )


def build_quality_points(periods: Iterable[DashboardPeriod]) -> tuple[QualityPoint, ...]:
    return tuple(
        QualityPoint(
            period=item.period,
            match_rate=item.match_rate,
            change_rate=item.change_rate,
        )
        for item in periods
    )
