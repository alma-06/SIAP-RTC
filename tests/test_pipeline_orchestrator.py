from app.dashboard.model import DashboardPeriod
from app.pipeline.orchestrator import run_executive_pipeline, run_history


def period(name: str) -> DashboardPeriod:
    return DashboardPeriod(name, 100, 10, 5, 80, 5, 0.80, 0.05, 0.10, 0.05, True, (), f"EV-{name}")


def test_pipeline_builds_and_verifies_complete_package(tmp_path) -> None:
    result = run_executive_pipeline(period("2026-Q2"), tmp_path)
    assert result.fact_sheet.kpis.period == "2026-Q2"
    assert result.payload.evidence_id == "EV-2026-Q2"
    assert result.verification.valid is True
    assert len(result.manifest.files) == 3


def test_history_creates_one_package_per_period(tmp_path) -> None:
    results = run_history((period("Q1"), period("Q2")), tmp_path)
    assert [result.period.period for result in results] == ["Q1", "Q2"]
    assert all(result.verification.valid for result in results)
