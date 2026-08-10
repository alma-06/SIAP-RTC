from __future__ import annotations

from pathlib import Path
import sqlite3
from collections.abc import Mapping

from app.domain.record_identity import record_identity_hash
from app.domain.query_filters import HistoricalQueryFilters


ALLOWED_SORT_COLUMNS = {
    "fecha": "fecha", "estado": "estado", "campana": "campana",
    "version": "version", "clave": "clave", "canal_base": "canal_base",
    "orden": "orden", "batch_id": "source_batch_id", "source_filename": "source_filename",
}

COLUMNS = (
    "id", "identity_hash", "pauta_transmision", "estado", "tiempo_fiscal",
    "canal_base", "orden", "fecha", "dependencia_cam_sen", "clave",
    "campana", "version", "source_batch_id", "source_filename", "created_at"
)


class HistoricalRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS historical_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    identity_hash TEXT NOT NULL UNIQUE,
                    pauta_transmision TEXT,
                    estado TEXT,
                    tiempo_fiscal TEXT,
                    canal_base TEXT,
                    orden TEXT,
                    fecha TEXT,
                    dependencia_cam_sen TEXT,
                    clave TEXT,
                    campana TEXT,
                    version TEXT,
                    source_batch_id TEXT NOT NULL,
                    source_filename TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(source_batch_id) REFERENCES import_batches(batch_id)
                );
                CREATE INDEX IF NOT EXISTS idx_historical_fecha ON historical_records(fecha);
                CREATE INDEX IF NOT EXISTS idx_historical_campana ON historical_records(campana);
                CREATE INDEX IF NOT EXISTS idx_historical_source_batch ON historical_records(source_batch_id);
                CREATE INDEX IF NOT EXISTS idx_historical_version ON historical_records(version);
                CREATE INDEX IF NOT EXISTS idx_historical_canal ON historical_records(canal_base);
                CREATE INDEX IF NOT EXISTS idx_historical_clave ON historical_records(clave);
                """
            )

    def insert_if_new(self, record: Mapping[str, object], *, batch_id: str, source_filename: str) -> bool:
        identity_hash = record_identity_hash(record)
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO historical_records(
                    identity_hash, pauta_transmision, estado, tiempo_fiscal,
                    canal_base, orden, fecha, dependencia_cam_sen, clave,
                    campana, version, source_batch_id, source_filename
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    identity_hash, record.get("pauta_transmision"), record.get("estado"),
                    record.get("tiempo_fiscal"), record.get("canal_base"), record.get("orden"),
                    record.get("fecha"), record.get("dependencia_cam_sen"), record.get("clave"),
                    record.get("campana"), record.get("version"), batch_id, source_filename,
                ),
            )
        return cursor.rowcount == 1

    def _where_clause(self, filters: HistoricalQueryFilters) -> tuple[str, list[object]]:
        where: list[str] = []
        params: list[object] = []
        if filters.date_from:
            where.append("date(fecha) >= date(?)")
            params.append(filters.date_from.isoformat())
        if filters.date_to:
            where.append("date(fecha) <= date(?)")
            params.append(filters.date_to.isoformat())
        for column, value in (
            ("estado", filters.estado), ("campana", filters.campana),
            ("version", filters.version), ("clave", filters.clave),
            ("canal_base", filters.canal_base), ("source_batch_id", filters.batch_id),
            ("source_filename", filters.source_filename),
        ):
            if value:
                where.append(f"{column} = ?")
                params.append(value)
        return (f" WHERE {' AND '.join(where)}" if where else ""), params

    def search(self, filters: HistoricalQueryFilters) -> tuple[list[dict[str, object]], int]:
        where_sql, params = self._where_clause(filters)
        order_column = ALLOWED_SORT_COLUMNS.get(filters.sort_by)
        if not order_column:
            raise ValueError(f"sort_by no permitido: {filters.sort_by}")
        direction = "DESC" if filters.descending else "ASC"
        columns = ", ".join(COLUMNS)
        with self._connect() as connection:
            total = connection.execute(
                f"SELECT COUNT(*) FROM historical_records{where_sql}", params
            ).fetchone()[0]
            rows = connection.execute(
                f"SELECT {columns} FROM historical_records{where_sql} "
                f"ORDER BY {order_column} {direction}, id ASC LIMIT ? OFFSET ?",
                [*params, filters.limit, filters.offset],
            ).fetchall()
        return [dict(row) for row in rows], total

    def metrics(self, filters: HistoricalQueryFilters) -> dict[str, object]:
        where_sql, params = self._where_clause(filters)

        def grouped(expression: str, dimension: str) -> list[dict[str, object]]:
            with self._connect() as connection:
                rows = connection.execute(
                    f"SELECT {expression} AS value, COUNT(*) AS count "
                    f"FROM historical_records{where_sql} "
                    f"GROUP BY {expression} ORDER BY count DESC, value ASC",
                    params,
                ).fetchall()
            return [{"dimension": dimension, "value": row["value"] or "(SIN DATO)", "count": row["count"]} for row in rows]

        with self._connect() as connection:
            total = connection.execute(
                f"SELECT COUNT(*) FROM historical_records{where_sql}", params
            ).fetchone()[0]
            duplicate_sql = "SELECT COUNT(*) FROM duplicate_audit"
            duplicates = connection.execute(duplicate_sql).fetchone()[0]

        return {
            "total": total,
            "by_period": grouped("substr(fecha, 1, 7)", "periodo"),
            "by_campaign": grouped("campana", "campana"),
            "by_version": grouped("version", "version"),
            "by_channel": grouped("canal_base", "canal_base"),
            "by_state": grouped("estado", "estado"),
            "by_key": grouped("clave", "clave"),
            "by_batch": grouped("source_batch_id", "batch_id"),
            "duplicates": duplicates,
        }
