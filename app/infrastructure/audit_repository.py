from __future__ import annotations

from pathlib import Path
import sqlite3

from app.ui.import_result import FileImportResult, ImportBatchResult


class AuditRepository:
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
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS import_batches (
                    batch_id TEXT PRIMARY KEY,
                    started_at TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('INICIADO','PROCESADO','ERROR'))
                );
                CREATE TABLE IF NOT EXISTS import_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id TEXT NOT NULL REFERENCES import_batches(batch_id) ON DELETE CASCADE,
                    filename TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    status TEXT NOT NULL,
                    records_read INTEGER NOT NULL DEFAULT 0,
                    cam_sen_records INTEGER NOT NULL DEFAULT 0,
                    duplicates INTEGER NOT NULL DEFAULT 0,
                    rejected INTEGER NOT NULL DEFAULT 0,
                    new_records INTEGER NOT NULL DEFAULT 0,
                    error TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_import_files_batch ON import_files(batch_id);
                CREATE INDEX IF NOT EXISTS idx_import_files_sha256 ON import_files(sha256);
                """
            )

    def save_batch(self, batch: ImportBatchResult) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO import_batches(batch_id, started_at, status) VALUES (?, ?, ?)",
                (batch.batch_id, batch.started_at.isoformat(), batch.status),
            )
            connection.execute("DELETE FROM import_files WHERE batch_id = ?", (batch.batch_id,))
            connection.executemany(
                """
                INSERT INTO import_files(
                    batch_id, filename, sha256, status, records_read,
                    cam_sen_records, duplicates, rejected, new_records, error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        batch.batch_id,
                        item.filename,
                        item.sha256,
                        item.status,
                        item.records_read,
                        item.cam_sen_records,
                        item.duplicates,
                        item.rejected,
                        item.new_records,
                        item.error,
                    )
                    for item in batch.files
                ],
            )

    def get_batch(self, batch_id: str) -> dict | None:
        with self._connect() as connection:
            batch = connection.execute(
                "SELECT batch_id, started_at, status FROM import_batches WHERE batch_id = ?",
                (batch_id,),
            ).fetchone()
            if not batch:
                return None
            files = connection.execute(
                """SELECT filename, sha256, status, records_read, cam_sen_records,
                          duplicates, rejected, new_records, error
                   FROM import_files WHERE batch_id = ? ORDER BY id""",
                (batch_id,),
            ).fetchall()
        return {
            "batch_id": batch[0],
            "started_at": batch[1],
            "status": batch[2],
            "files": [dict(zip(
                ["filename", "sha256", "status", "records_read", "cam_sen_records", "duplicates", "rejected", "new_records", "error"],
                row,
            )) for row in files],
        }
