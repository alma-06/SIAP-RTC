from app.pipeline.deduplicate import deduplicate_records
from app.pipeline.rtc_ingest import IngestedRecord


def record(source: str, order: str) -> IngestedRecord:
    values = {
        "Pauta de transmisión": "pauta",
        "Estado": "programada",
        "Tiempo Fiscal": 30,
        "Canal Base": "am",
        "Orden": order,
        "Fecha": "2026-08-11",
        "Dependencia CAM. SEN.": "cam. sen.",
        "Clave": "c1",
        "Campaña": "campaña",
        "Versión": "v1",
    }
    return IngestedRecord(source, values)


def test_deduplication_removes_only_exact_duplicate() -> None:
    result = deduplicate_records([record("a.xlsx", "o1"), record("b.xlsx", "o1"), record("b.xlsx", "o2")])
    assert len(result.records) == 2
    assert [item.values["Orden"] for item in result.records] == ["o1", "o2"]
    assert [item.action for item in result.decisions] == ["keep", "drop", "keep"]
    assert "duplicado exacto" in result.decisions[1].reason
