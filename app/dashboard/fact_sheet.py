from __future__ import annotations

from dataclasses import dataclass

from app.dashboard.alerts import DashboardAlert, build_alerts
from app.dashboard.kpis import ExecutiveKpis, build_executive_kpis
from app.dashboard.model import DashboardPeriod


@dataclass(frozen=True)
class ExecutiveFactSheet:
    kpis: ExecutiveKpis
    alerts: tuple[DashboardAlert, ...]
    status_label: str


def build_fact_sheet(period: DashboardPeriod) -> ExecutiveFactSheet:
    status_label = "COMPARABLE" if period.comparable else "NO COMPARABLE"
    return ExecutiveFactSheet(
        kpis=build_executive_kpis(period),
        alerts=build_alerts(period),
        status_label=status_label,
    )
