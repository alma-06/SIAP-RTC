from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from collections.abc import Iterator, Mapping
from datetime import datetime, timezone
import sqlite3

from app.domain.record_identity import record_identity_hash


class ImportTransaction:
    """Coordinates an RTC batch, historical inserts and duplicate evidence transactionally."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @contextmanager
    def begin(self, batch_id: str, started_at: datetime | None = None) -> Iterator[sqlite3.Connection]:
        connection = self._connect()
        try:
            connection.execute("BEGIN")
            connection.execute(
                """
                INSERT INTO import_batches(batch_id, started_at, status)
                VALUES (?, ?, 'INICIADO')
                """,
                (batch_id, (started_at or datetime.now(timezone.utc)).isoformat()),
            )
            yield connection
            connection.execute(
                "UPDATE import_batches SET status = 'PROCESADO' WHERE batch_id = ?",
                (batch_id,),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def insert_record_or_audit_duplicate(
        connection: sqlite3.Connection,
        record: Mapping[str, object],
        *,
        batch_id: str,
        source_filename: str,
    ) -> bool:
        identity_hash = record_identity_hash(record)
        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO historical_records(
                identity_hash, pauta_transmision, estado, tiempo_fiscal,
                canal_base, orden, fecha, dependencia_cam_sen, clave,
                campana, version, source_batch_id, source_filename
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                identity_hash,
                record.get("pauta_transmision"),
                record.get("estado"),
                record.get("tiempo_fiscal"),
                record.get("canal_base"),
                record.get("orden"),
                record.get("fecha"),
                record.get("dependencia_cam_sen"),
                record.get("clave"),
                record.get("campana"),
                record.get("version"),
                batch_id,
                source_filename,
            ),
        )
        if cursor.rowcount == 1:
            return True

        existing = connection.execute(
            "SELECT id FROM historical_records WHERE identity_hash = ?",
            (identity_hash,),
        ).fetchone()
        connection.execute(
            """
            INSERT OR IGNORE INTO duplicate_audit(
                identity_hash, batch_id, source_filename, existing_record_id
            ) VALUES (?, ?, ?, ?)
            """,
            (identity_hash, batch_id, source_filename, existing[0] if existing else None),
        )
        return False
