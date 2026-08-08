from __future__ import annotations

from pathlib import Path
import sqlite3


class DuplicateAuditRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS duplicate_audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    identity_hash TEXT NOT NULL,
                    batch_id TEXT NOT NULL REFERENCES import_batches(batch_id),
                    source_filename TEXT NOT NULL,
                    existing_record_id INTEGER,
                    detected_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(identity_hash, batch_id, source_filename)
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_duplicate_audit_batch ON duplicate_audit(batch_id)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_duplicate_audit_identity ON duplicate_audit(identity_hash)"
            )

    def record_duplicate(
        self,
        *,
        identity_hash: str,
        batch_id: str,
        source_filename: str,
        existing_record_id: int | None = None,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO duplicate_audit(
                    identity_hash, batch_id, source_filename, existing_record_id
                ) VALUES (?, ?, ?, ?)
                """,
                (identity_hash, batch_id, source_filename, existing_record_id),
            )

    def count_for_batch(self, batch_id: str) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) FROM duplicate_audit WHERE batch_id = ?",
                (batch_id,),
            ).fetchone()
        return int(row[0]) if row else 0
