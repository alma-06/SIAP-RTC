from app.reconciliation.change_audit import build_change_audit_entries
from app.reconciliation.content_diff import ContentStatus, FieldDifference, ContentComparison


def test_changed_content_creates_one_audit_entry_per_field() -> None:
    comparison = ContentComparison(
        identity_hash="A",
        status=ContentStatus.CHANGED,
        differences=(FieldDifference("version", "01", "02"), FieldDifference("campaign", "X", "Y")),
    )
    entries = build_change_audit_entries(
        comparison,
        source_file="pauta_2026_08.xlsx",
        previous_source_file="pauta_2026_07.xlsx",
        import_batch_id="BATCH-001",
        detected_at="2026-08-10T12:00:00+00:00",
    )
    assert len(entries) == 2
    assert entries[0].identity_hash == "A"
    assert entries[0].previous_value == "01"
    assert entries[0].current_value == "02"
    assert entries[0].import_batch_id == "BATCH-001"


def test_identical_content_creates_no_audit_entries() -> None:
    comparison = ContentComparison("A", ContentStatus.IDENTICAL, ())
    assert build_change_audit_entries(comparison, "pauta.xlsx") == ()
