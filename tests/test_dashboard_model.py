import pytest

from app.dashboard.model import build_dashboard_model
from app.reconciliation.evidence import ReconciliationEvidence
from app.reconciliation.period_series import PeriodReconciliation
from app.reconciliation.summary import ReconciliationSummary


def test_dashboard_consumes_validated_summary_and_evidence() -> None:
    summary = ReconciliationSummary(10, 2, 1, 6, 1)
    evidence = ReconciliationEvidence(
        evidence_id="EV-001",
        period="2026-Q2",
        source_file="pauta.xlsx",
        source_hash="abc",
        universe_id="U1",
        methodology_id="M1",
        record_count=10,
        summary=summary,
        comparable=True,
        warnings=(),
        generated_at="2026-08-10T12:00:00+00:00",
    )
    model = build_dashboard_model(
        (PeriodReconciliation("2026-Q2", summary),),
        (evidence,),
    )
    assert model.latest is not None
    assert model.latest.evidence_id == "EV-001"
    assert model.latest.match_rate == 0.6


def test_dashboard_requires_evidence_for_every_period() -> None:
    summary = ReconciliationSummary(1, 0, 0, 1, 0)
    with pytest.raises(ValueError, match="Falta evidencia"):
        build_dashboard_model((PeriodReconciliation("2026-Q2", summary),), ())
