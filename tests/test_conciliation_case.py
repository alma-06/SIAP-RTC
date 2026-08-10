from app.methodology.broadcaster_universe import BroadcasterUniverse
from app.methodology.conciliation_case import ConciliationCase


def test_conciliation_case_reconstructs_calculation() -> None:
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
            source_file="estaciones_q2_2026.xlsx",
        ),
        impacts=10,
    )
    evidence = case.evidence_summary()
    assert evidence["total_seconds"] == 413100
    assert evidence["elapsed_time"] == "114:45:00"
    assert evidence["source_hash"] == "sha256:fixture"
    assert evidence["universe_id"] == "CRT-2026-Q2"
