from app.reconciliation.comparability import ComparabilityResult
from app.reconciliation.evidence import build_reconciliation_evidence
from app.reconciliation.summary import ReconciliationSummary


def test_evidence_binds_source_metadata_and_summary() -> None:
    summary = ReconciliationSummary(10, 2, 1, 6, 1)
    evidence = build_reconciliation_evidence(
        period="2026-Q2",
        source_file="pauta_q2.xlsx",
        source_hash="abc123",
        universe_id="CRT-2026-Q2",
        methodology_id="M1",
        record_count=10,
        summary=summary,
        comparability=ComparabilityResult(False, ("Universo distinto",)),
        generated_at="2026-08-10T12:00:00+00:00",
        additional_warnings=("Advertencia manual",),
    )
    assert evidence.evidence_id == "8e22d99c8f6a3a7d"
    assert evidence.source_hash == "abc123"
    assert evidence.summary is summary
    assert evidence.comparable is False
    assert evidence.warnings == ("Advertencia manual", "Universo distinto")
