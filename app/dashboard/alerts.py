from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from app.dashboard.model import DashboardPeriod


class AlertLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"


@dataclass(frozen=True)
class DashboardAlert:
    code: str
    level: AlertLevel
    period: str
    message: str


def build_alerts(
    period: DashboardPeriod,
    *,
    modification_rate_warning: float = 0.25,
    removal_rate_warning: float = 0.25,
) -> tuple[DashboardAlert, ...]:
    alerts: list[DashboardAlert] = []
    if not period.comparable:
        alerts.append(DashboardAlert("NON_COMPARABLE", AlertLevel.WARNING, period.period, "El periodo no es comparable con el universo o metodología de referencia."))
    if period.warnings:
        alerts.append(DashboardAlert("EVIDENCE_WARNING", AlertLevel.WARNING, period.period, f"Existen {len(period.warnings)} advertencia(s) asociada(s) a la evidencia."))
    if period.change_rate >= modification_rate_warning:
        alerts.append(DashboardAlert("HIGH_MODIFICATION_RATE", AlertLevel.WARNING, period.period, "La tasa de modificación alcanza o supera el umbral de revisión."))
    if period.removal_rate >= removal_rate_warning:
        alerts.append(DashboardAlert("HIGH_REMOVAL_RATE", AlertLevel.WARNING, period.period, "La tasa de remoción/ausencia alcanza o supera el umbral de revisión."))
    return tuple(alerts)


def build_alerts_for_periods(periods: Iterable[DashboardPeriod]) -> tuple[DashboardAlert, ...]:
    alerts: list[DashboardAlert] = []
    for period in periods:
        alerts.extend(build_alerts(period))
    return tuple(alerts)
