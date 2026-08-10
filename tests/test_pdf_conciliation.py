from app.exports.pdf_conciliation import build_pdf_conciliation_document
from app.methodology.broadcaster_universe import BroadcasterUniverse
from app.methodology.conciliation_case import ConciliationCase


def test_pdf_document_uses_canonical_report_content() -> None:
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
    document = build_pdf_conciliation_document(case)
    assert document.title.endswith("C78-2026-Q2-001")
    assert "114:45:00" in document.markdown_source
    assert "sha256:fixture" in document.markdown_source
    assert "Interpretación y limitaciones" in document.markdown_source
