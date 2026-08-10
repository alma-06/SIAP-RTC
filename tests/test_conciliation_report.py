from app.methodology.broadcaster_universe import BroadcasterUniverse
from app.methodology.conciliation_case import ConciliationCase
from app.methodology.conciliation_report import build_conciliation_report


def test_report_contains_reproducible_evidence() -> None:
    case = ConciliationCase(
        case_id="C78-2026-Q2-001",
        period="2026-Q2",
        source_file="pauta_q2_2026.xlsx",
        source_hash="sha256:fixture",
        universe=BroadcasterUniverse(
            universe_id="CRT-2026-Q2",
            total_stations=1377,
            source="Base CRT",
            cutoff_date="2026-06-30",
            methodology="Conteo de estaciones activas",
        ),
        impacts=10,
    )
    markdown = build_conciliation_report(case).to_markdown()
    assert "C78-2026-Q2-001" in markdown
    assert "sha256:fixture" in markdown
    assert "1,377" in markdown or "1377" in markdown
    assert "114:45:00" in markdown
    assert "impactos × radiodifusoras × duración estándar" in markdown
    assert "no constituye por sí mismo evidencia" in markdown
