from app.dashboard.fact_sheet import build_fact_sheet
from app.dashboard.model import DashboardPeriod


def test_fact_sheet_contains_kpis_alerts_and_status() -> None:
    period = DashboardPeriod(
        "2026-Q2", 100, 10, 30, 55, 5, 0.55, 0.05, 0.10, 0.30,
        False, ("Universo distinto",), "EV-01"
    )
    sheet = build_fact_sheet(period)
    assert sheet.status_label == "NO COMPARABLE"
    assert sheet.kpis.total_compared == 100
    assert sheet.kpis.evidence_id == "EV-01"
    assert {a.code for a in sheet.alerts} == {"NON_COMPARABLE", "EVIDENCE_WARNING", "HIGH_REMOVAL_RATE"}
