from pathlib import Path
import sqlite3

from app.application.historical_metrics_service import HistoricalMetricsService
from app.domain.query_filters import HistoricalQueryFilters
from app.infrastructure.historical_repository import HistoricalRepository


def setup_db(path: Path) -> None:
    with sqlite3.connect(path) as c:
        c.executescript('''
        CREATE TABLE import_batches (batch_id TEXT PRIMARY KEY, started_at TEXT NOT NULL, status TEXT NOT NULL);
        CREATE TABLE duplicate_audit (
            id INTEGER PRIMARY KEY, identity_hash TEXT, batch_id TEXT, source_filename TEXT,
            existing_record_id INTEGER, detected_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(identity_hash,batch_id,source_filename)
        );
        INSERT INTO import_batches VALUES ('B-001','2026-08-01T00:00:00+00:00','PROCESADO');
        INSERT INTO import_batches VALUES ('B-002','2026-08-02T00:00:00+00:00','PROCESADO');
        CREATE TABLE historical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT, identity_hash TEXT UNIQUE NOT NULL,
            pauta_transmision TEXT, estado TEXT, tiempo_fiscal TEXT, canal_base TEXT, orden TEXT,
            fecha TEXT, dependencia_cam_sen TEXT, clave TEXT, campana TEXT, version TEXT,
            source_batch_id TEXT, source_filename TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        INSERT INTO historical_records(identity_hash,estado,canal_base,fecha,clave,campana,version,source_batch_id,source_filename)
        VALUES ('h1','ACTIVO','AM-1','2026-08-01','K1','C1','V1','B-001','a.xlsx');
        INSERT INTO historical_records(identity_hash,estado,canal_base,fecha,clave,campana,version,source_batch_id,source_filename)
        VALUES ('h2','ACTIVO','AM-2','2026-08-02','K2','C1','V2','B-002','b.xlsx');
        INSERT INTO historical_records(identity_hash,estado,canal_base,fecha,clave,campana,version,source_batch_id,source_filename)
        VALUES ('h3','INACTIVO','AM-1','2026-08-02','K1','C2','V1','B-002','b.xlsx');
        INSERT INTO duplicate_audit(identity_hash,batch_id,source_filename) VALUES ('h1','B-002','b.xlsx');
        ''')


def test_metrics_group_history(tmp_path: Path) -> None:
    db = tmp_path / 'db.sqlite'
    setup_db(db)
    service = HistoricalMetricsService(HistoricalRepository(db))
    metrics = service.summarize()

    assert metrics.total == 3
    assert {(item.value, item.count) for item in metrics.by_campaign} == {('C1', 2), ('C2', 1)}
    assert {(item.value, item.count) for item in metrics.by_channel} == {('AM-1', 2), ('AM-2', 1)}
    assert {(item.value, item.count) for item in metrics.by_period} == {('2026-08', 3)}
    assert metrics.duplicates == 1


def test_metrics_respect_query_filters(tmp_path: Path) -> None:
    db = tmp_path / 'db.sqlite'
    setup_db(db)
    service = HistoricalMetricsService(HistoricalRepository(db))
    metrics = service.summarize(HistoricalQueryFilters(campana='C1'))
    assert metrics.total == 2
    assert {(item.value, item.count) for item in metrics.by_version} == {('V1', 1), ('V2', 1)}
