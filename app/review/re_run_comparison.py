from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class MetricDelta:
    name: str
    previous: float
    current: float

    @property
    def delta(self) -> float:
        return self.current - self.previous


@dataclass(frozen=True)
class RerunComparison:
    previous_run_id: str
    current_run_id: str
    metrics: tuple[MetricDelta, ...]


def compare_runs(
    previous_run_id: str,
    current_run_id: str,
    previous: Mapping[str, float],
    current: Mapping[str, float],
) -> RerunComparison:
    names = sorted(set(previous) | set(current))
    metrics = tuple(
        MetricDelta(name, float(previous.get(name, 0)), float(current.get(name, 0)))
        for name in names
    )
    return RerunComparison(previous_run_id, current_run_id, metrics)
