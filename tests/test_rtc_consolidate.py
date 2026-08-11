from app.pipeline.consolidate import consolidate_history, consolidate_records
from app.pipeline.rtc_ingest import IngestedRecord


def record(source: str) -> IngestedRecord:
    return IngestedRecord(source, {"Orden": "o1"})


def test_consolidate_records_preserves_period_and_source() -> None:
    result = consolidate_records([record("a.xlsx"), record("b.xlsx")], "2026-Q2")
    assert len(result.records) == 2
    assert result.periods == ("2026-Q2",)
    assert result.source_files == ("a.xlsx", "b.xlsx")
    assert result.records[0].period == "2026-Q2"


def test_consolidate_history_keeps_period_and_file_provenance() -> None:
    result = consolidate_history([
        ("2026-Q1", [record("q1.xlsx")]),
        ("2026-Q2", [record("q2.xlsx")]),
    ])
    assert result.periods == ("2026-Q1", "2026-Q2")
    assert result.source_files == ("q1.xlsx", "q2.xlsx")
    assert [item.period for item in result.records] == ["2026-Q1", "2026-Q2"]
