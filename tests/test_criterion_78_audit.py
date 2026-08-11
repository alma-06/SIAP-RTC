from app.methodology.criterion_78 import Criterion78Parameters
from app.methodology.criterion_78_audit import calculate_criterion_78_audited


def test_criterion_78_audit_preserves_parameters_and_fingerprint() -> None:
    parameters = Criterion78Parameters(
        broadcaster_count=1377,
        standard_spot_seconds=30,
        impacts_per_day=10,
        parameter_source="CRT",
        cutoff_date="2026-06-30",
    )
    result, audit = calculate_criterion_78_audited("2026-Q2", 10, parameters)
    assert result.total_seconds == 10 * 1377 * 30
    assert audit.result_type == "calculado"
    assert audit.parameter_source == "CRT"
    assert audit.cutoff_date == "2026-06-30"
    assert len(audit.input_fingerprint) == 64
    assert "no constituye por sí mismo evidencia" in audit.interpretation
