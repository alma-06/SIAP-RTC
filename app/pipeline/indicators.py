from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.pipeline.reconcile import ReconciliationDecision, ReconciliationResult


@dataclass(frozen=True)
class IndicatorResult:
    previous_count: int
    current_count: int
    unchanged_count: int
    added_count: int
    removed_count: int
    modified_count: int
    net_change: int
    retention_rate: float | None
    added_rate: float | None
    removed_rate: float | None
    modified_rate: float | None


def _rate(numerator: int, denominator: int) -> float | None:
    return None if denominator == 0 else numerator / denominator


def build_indicators(result: ReconciliationResult) -> IndicatorResult:
    return IndicatorResult(
        previous_count=result.previous_count,
        current_count=result.current_count,
        unchanged_count=result.unchanged_count,
        added_count=result.added_count,
        removed_count=result.removed_count,
        modified_count=result.modified_count,
        net_change=result.current_count - result.previous_count,
        retention_rate=_rate(result.unchanged_count, result.previous_count),
        added_rate=_rate(result.added_count, result.current_count),
        removed_rate=_rate(result.removed_count, result.previous_count),
        modified_rate=_rate(result.modified_count, result.current_count),
    )


def indicator_summary(result: ReconciliationResult) -> dict[str, int | float | None]:
    indicators = build_indicators(result)
    return {
        "previous_count": indicators.previous_count,
        "current_count": indicators.current_count,
        "unchanged_count": indicators.unchanged_count,
        "added_count": indicators.added_count,
        "removed_count": indicators.removed_count,
        "modified_count": indicators.modified_count,
        "net_change": indicators.net_change,
        "retention_rate": indicators.retention_rate,
        "added_rate": indicators.added_rate,
        "removed_rate": indicators.removed_rate,
        "modified_rate": indicators.modified_rate,
    }
