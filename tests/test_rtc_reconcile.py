from app.pipeline.consolidate import ConsolidatedRecord
from app.pipeline.reconcile import reconcile_periods
from app.pipeline.rtc_ingest import IngestedRecord


def record(source: str, order: str, version: str = "v1") -> ConsolidatedRecord:
    values = {
        "Orden": order,
        "Fecha": "2026-08-11",
        "Clave": "c1",
        "Campaña": "campaña",
        "Versión": version,
        "Canal Base": "am",
    }
    return ConsolidatedRecord("periodo", source, IngestedRecord(source, values))


def test_reconcile_classifies_added_removed_unchanged_and_modified() -> None:
    previous = [record("old.xlsx", "o1"), record("old.xlsx", "o2"), record("old.xlsx", "o3")]
    current = [record("new.xlsx", "o1"), record("new.xlsx", "o2", "v2"), record("new.xlsx", "o4")]
    result = reconcile_periods(previous, current)
    classes = {item.classification for item in result.decisions}
    assert classes == {"unchanged", "modified", "removed", "added"}
    assert result.unchanged_count == 1
    assert result.added_count == 1
    assert result.removed_count == 1
    assert result.modified_count == 1
    modified = next(item for item in result.decisions if item.classification == "modified")
    assert modified.changed_fields == ("Versión",)
