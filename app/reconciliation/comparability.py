from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PeriodMethodology:
    period: str
    universe_id: str
    methodology_id: str
    comparable_fields: tuple[str, ...]


@dataclass(frozen=True)
class ComparabilityResult:
    comparable: bool
    reasons: tuple[str, ...]


def validate_period_comparability(periods: Iterable[PeriodMethodology]) -> ComparabilityResult:
    items = tuple(periods)
    if len(items) <= 1:
        return ComparabilityResult(True, ())

    reasons: list[str] = []
    first = items[0]
    for item in items[1:]:
        if item.universe_id != first.universe_id:
            reasons.append(f"Universo distinto: {first.period} vs {item.period}")
        if item.methodology_id != first.methodology_id:
            reasons.append(f"Metodología distinta: {first.period} vs {item.period}")
        if item.comparable_fields != first.comparable_fields:
            reasons.append(f"Campos comparables distintos: {first.period} vs {item.period}")

    return ComparabilityResult(not reasons, tuple(reasons))
