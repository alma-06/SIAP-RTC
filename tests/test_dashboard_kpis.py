from app.dashboard.kpis import build_executive_kpis
from app.dashboard.model import DashboardPeriod


def test_kpis_select_without_recalculating() -> None:
    period = DashboardPeriod(
        period="2026-Q2",
        total_compared=100,
        additions=10,
        removals=5,
        persistence=80,
        modifications=5,
        match_rate=0.80,
        change_rate=0.05,
        addition_rate=0.10,
        removal_rate=0.05,
        comparable=True,
        warnings=("warning",),
        evidence_id="EV-01",
    )
    kpis = build_executive_kpis(period)
    assert kpis.total_compared == 100
    assert kpis.additions == 10
    assert kpis.modifications == 5
    assert kpis.persistence == 80
    assert kpis.removals == 5
    assert kpis.match_rate == 0.80
    assert kpis.change_rate == 0.05
    assert kpis.warnings_count == 1
    assert kpis.evidence_id == "EV-01"
