import pytest

from app.dashboard.model import DashboardPeriod
from app.dashboard.selection import select_dashboard_periods


def p(name: str) -> DashboardPeriod:
    return DashboardPeriod(name, 10, 1, 1, 7, 1, 0.7, 0.1, 0.1, 0.1, True, (), f"EV-{name}")


def test_selects_current_reference_and_history() -> None:
    result = select_dashboard_periods((p("Q1"), p("Q2"), p("Q3")), "Q3", "Q2", ("Q1", "Q2", "Q3"))
    assert result.current.period == "Q3"
    assert result.reference is not None and result.reference.period == "Q2"
    assert [item.period for item in result.history] == ["Q1", "Q2", "Q3"]


def test_rejects_same_current_and_reference() -> None:
    with pytest.raises(ValueError, match="deben ser distintos"):
        select_dashboard_periods((p("Q1"),), "Q1", "Q1")


def test_rejects_unknown_period() -> None:
    with pytest.raises(ValueError, match="No existe el periodo actual"):
        select_dashboard_periods((p("Q1"),), "Q2")
