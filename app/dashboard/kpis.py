from __future__ import annotations

from dataclasses import dataclass

from app.dashboard.model import DashboardPeriod


@dataclass(frozen=True)
class ExecutiveKpis:
    period: str
    total_compared: int
    additions: int
    modifications: int
    persistence: int
    removals: int
    match_rate: float
    change_rate: float
    comparable: bool
    warnings_count: int
    evidence_id: str


def build_executive_kpis(period: DashboardPeriod) -> ExecutiveKpis:
    """Select presentation KPIs without recalculating reconciliation results."""
    return ExecutiveKpis(
        period=period.period,
        total_compared=period.total_compared,
        additions=period.additions,
        modifications=period.modifications,
        persistence=period.persistence,
        removals=period.removals,
        match_rate=period.match_rate,
        change_rate=period.change_rate,
        comparable=period.comparable,
        warnings_count=len(period.warnings),
        evidence_id=period.evidence_id,
    )
