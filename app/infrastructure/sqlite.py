"""SQLite infrastructure adapter for SIAP-RTC repositories."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from uuid import UUID

from app.domain.entities import ImportBatch, RtcSourceFile
from app.domain.repositories import ImportBatchRepository, SourceFileRepository


class SQLiteConnection:
    """Small connection factory kept outside the domain layer."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection


class SQLiteSourceFileRepository(SourceFileRepository):
    """SQLite adapter for source-file persistence."""

    def __init__(self, connection: SQLiteConnection) -> None:
        self._connection = connection

    def add(self, source_file: RtcSourceFile) -> None:
        with self._connection.connect() as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS rtc_source_file (
                    id TEXT PRIMARY KEY,
                    path TEXT NOT NULL,
                    sha256 TEXT NOT NULL UNIQUE,
                    received_at TEXT NOT NULL
                )
                """
            )
            db.execute(
                "INSERT INTO rtc_source_file (id, path, sha256, received_at) VALUES (?, ?, ?, ?)",
                (str(source_file.id), str(source_file.path), source_file.sha256.value,
                 source_file.received_at.isoformat()),
            )
            db.commit()

    def get(self, source_file_id: UUID) -> RtcSourceFile | None:
        # Full reconstruction is introduced with the migration layer in PMI-02.
        return None


class SQLiteImportBatchRepository(ImportBatchRepository):
    """SQLite adapter for import-batch persistence."""

    def __init__(self, connection: SQLiteConnection) -> None:
        self._connection = connection

    def add(self, batch: ImportBatch) -> None:
        with self._connection.connect() as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS import_batch (
                    id TEXT PRIMARY KEY,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    imported_count INTEGER NOT NULL DEFAULT 0,
                    rejected_count INTEGER NOT NULL DEFAULT 0,
                    duplicate_count INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            db.execute(
                """
                INSERT INTO import_batch
                (id, started_at, finished_at, imported_count, rejected_count, duplicate_count)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    finished_at=excluded.finished_at,
                    imported_count=excluded.imported_count,
                    rejected_count=excluded.rejected_count,
                    duplicate_count=excluded.duplicate_count
                """,
                (str(batch.id), batch.started_at.isoformat(),
                 batch.finished_at.isoformat() if batch.finished_at else None,
                 batch.imported_count, batch.rejected_count, batch.duplicate_count),
            )
            db.commit()

    def get(self, batch_id: UUID) -> ImportBatch | None:
        return None
