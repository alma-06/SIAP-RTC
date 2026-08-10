import sqlite3

from app.reconciliation.audit_store import append_change_audit, initialize_audit_store
from app.reconciliation.change_audit import ChangeAuditEntry


def test_append_change_audit_persists_entries(tmp_path) -> None:
    db = tmp_path / "siap_rtc.sqlite3"
    initialize_audit_store(db)
    entries = [
        ChangeAuditEntry(
            identity_hash="A",
            source_file="new.xlsx",
            previous_source_file="old.xlsx",
            detected_at="2026-08-10T12:00:00+00:00",
            field="version",
            previous_value="01",
            current_value="02",
            import_batch_id="B1",
        )
    ]
    assert append_change_audit(db, entries) == 1
    with sqlite3.connect(db) as connection:
        row = connection.execute(
            "SELECT identity_hash, field, previous_value, current_value, import_batch_id FROM change_audit"
        ).fetchone()
    assert row == ("A", "version", "01", "02", "B1")
