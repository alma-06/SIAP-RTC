from app.dashboard.comparison import build_executive_comparison
from app.dashboard.model import DashboardPeriod


def p(period: str, comparable: bool = True) -> DashboardPeriod:
    return DashboardPeriod(period, 100, 10, 5, 80, 5, 0.8, 0.05, 0.1, 0.05, comparable, () if comparable else ("warning",), f"EV-{period}")


def test_comparison_preserves_periods_and_flags_non_comparable_rows() -> None:
    result = build_executive_comparison((p("2026-Q1"), p("2026-Q2", False)))
    assert [row.period for row in result.rows] == ["2026-Q1", "2026-Q2"]
    assert result.comparable is False
    assert result.warnings == ("2026-Q2: periodo no comparable",)
