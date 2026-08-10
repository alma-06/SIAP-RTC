from app.dashboard.charts import build_quality_points, build_trend_points
from app.dashboard.model import DashboardPeriod


def period(name: str, additions: int, modifications: int, persistence: int, removals: int) -> DashboardPeriod:
    total = additions + modifications + persistence + removals
    return DashboardPeriod(name, total, additions, removals, persistence, modifications, persistence / total, modifications / total, additions / total, removals / total, True, (), f"EV-{name}")


def test_trend_points_preserve_period_order_and_values() -> None:
    points = build_trend_points((period("Q1", 2, 1, 6, 1), period("Q2", 3, 2, 8, 2)))
    assert [p.period for p in points] == ["Q1", "Q2"]
    assert points[1].modifications == 2


def test_quality_points_expose_validated_rates() -> None:
    points = build_quality_points((period("Q1", 2, 1, 6, 1),))
    assert points[0].match_rate == 0.6
    assert points[0].change_rate == 0.1
