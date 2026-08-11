from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.dashboard.model import DashboardPeriod


@dataclass(frozen=True)
class DashboardSelection:
    current: DashboardPeriod
    reference: DashboardPeriod | None
    history: tuple[DashboardPeriod, ...]


def select_dashboard_periods(
    periods: Iterable[DashboardPeriod],
    current_period: str,
    reference_period: str | None = None,
    history_periods: Iterable[str] = (),
) -> DashboardSelection:
    items = tuple(periods)
    by_period = {item.period: item for item in items}
    if current_period not in by_period:
        raise ValueError(f"No existe el periodo actual: {current_period}")
    if reference_period == current_period:
        raise ValueError("El periodo actual y el periodo de referencia deben ser distintos")
    if reference_period is not None and reference_period not in by_period:
        raise ValueError(f"No existe el periodo de referencia: {reference_period}")

    requested_history = tuple(dict.fromkeys(history_periods))
    missing = [period for period in requested_history if period not in by_period]
    if missing:
        raise ValueError(f"No existe(n) periodo(s) histórico(s): {', '.join(missing)}")

    history = tuple(by_period[period] for period in requested_history)
    return DashboardSelection(
        current=by_period[current_period],
        reference=by_period.get(reference_period) if reference_period else None,
        history=history,
    )
