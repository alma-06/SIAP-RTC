from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

from app.reconciliation.change_audit import ChangeAuditEntry


SCHEMA = """
CREATE TABLE IF NOT EXISTS change_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    identity_hash TEXT NOT NULL,
    source_file TEXT NOT NULL,
    previous_source_file TEXT,
    detected_at TEXT NOT NULL,
    field TEXT NOT NULL,
    previous_value TEXT,
    current_value TEXT,
    change_type TEXT NOT NULL,
    import_batch_id TEXT
);
CREATE INDEX IF NOT EXISTS idx_change_audit_identity
    ON change_audit(identity_hash);
CREATE INDEX IF NOT EXISTS idx_change_audit_batch
    ON change_audit(import_batch_id);
"""


def initialize_audit_store(db_path: str | Path) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.executescript(SCHEMA)


def append_change_audit(db_path: str | Path, entries: Iterable[ChangeAuditEntry]) -> int:
    rows = [
        (
            entry.identity_hash,
            entry.source_file,
            entry.previous_source_file,
            entry.detected_at,
            entry.field,
            None if entry.previous_value is None else str(entry.previous_value),
            None if entry.current_value is None else str(entry.current_value),
            entry.change_type,
            entry.import_batch_id,
        )
        for entry in entries
    ]
    if not rows:
        return 0
    with sqlite3.connect(db_path) as connection:
        connection.executemany(
            """INSERT INTO change_audit
            (identity_hash, source_file, previous_source_file, detected_at,
             field, previous_value, current_value, change_type, import_batch_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            rows,
        )
        return len(rows)
