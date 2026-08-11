from app.dashboard.alerts import AlertLevel, build_alerts
from app.dashboard.model import DashboardPeriod


def make_period(*, comparable=True, warnings=(), change_rate=0.1, removal_rate=0.1):
    return DashboardPeriod("2026-Q2", 100, 10, 10, 75, 5, 0.75, change_rate, 0.1, removal_rate, comparable, warnings, "EV-1")


def test_non_comparable_and_warning_state_is_visible() -> None:
    alerts = build_alerts(make_period(comparable=False, warnings=("different universe",)))
    assert {alert.code for alert in alerts} == {"NON_COMPARABLE", "EVIDENCE_WARNING"}
    assert all(alert.level is AlertLevel.WARNING for alert in alerts)


def test_high_rates_trigger_review_alerts() -> None:
    alerts = build_alerts(make_period(change_rate=0.25, removal_rate=0.30))
    assert {alert.code for alert in alerts} == {"HIGH_MODIFICATION_RATE", "HIGH_REMOVAL_RATE"}


def test_rates_below_threshold_do_not_trigger_rate_alerts() -> None:
    alerts = build_alerts(make_period(change_rate=0.24, removal_rate=0.24))
    assert alerts == ()
