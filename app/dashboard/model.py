from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.reconciliation.evidence import ReconciliationEvidence
from app.reconciliation.period_series import PeriodReconciliation


@dataclass(frozen=True)
class DashboardPeriod:
    period: str
    total_compared: int
    additions: int
    removals: int
    persistence: int
    modifications: int
    match_rate: float
    change_rate: float
    addition_rate: float
    removal_rate: float
    comparable: bool
    warnings: tuple[str, ...]
    evidence_id: str


@dataclass(frozen=True)
class ExecutiveDashboardModel:
    periods: tuple[DashboardPeriod, ...]

    @property
    def latest(self) -> DashboardPeriod | None:
        return self.periods[-1] if self.periods else None


def build_dashboard_model(
    periods: Iterable[PeriodReconciliation],
    evidence: Iterable[ReconciliationEvidence],
) -> ExecutiveDashboardModel:
    evidence_by_period = {item.period: item for item in evidence}
    output: list[DashboardPeriod] = []
    for item in periods:
        evidence_item = evidence_by_period.get(item.period)
        if evidence_item is None:
            raise ValueError(f"Falta evidencia para el periodo {item.period}")
        summary = item.summary
        output.append(
            DashboardPeriod(
                period=item.period,
                total_compared=summary.total_compared,
                additions=summary.additions,
                removals=summary.removals,
                persistence=summary.persistence,
                modifications=summary.modifications,
                match_rate=summary.match_rate,
                change_rate=summary.change_rate,
                addition_rate=summary.addition_rate,
                removal_rate=summary.removal_rate,
                comparable=evidence_item.comparable,
                warnings=evidence_item.warnings,
                evidence_id=evidence_item.evidence_id,
            )
        )
    return ExecutiveDashboardModel(tuple(output))
