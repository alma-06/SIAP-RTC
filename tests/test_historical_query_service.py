from pathlib import Path
import sqlite3

from app.application.historical_query_service import HistoricalQueryService
from app.domain.query_filters import HistoricalQueryFilters
from app.infrastructure.historical_repository import HistoricalRepository


def setup_db(path: Path) -> None:
    with sqlite3.connect(path) as c:
        c.executescript('''
        CREATE TABLE import_batches (batch_id TEXT PRIMARY KEY, started_at TEXT NOT NULL, status TEXT NOT NULL);
        CREATE TABLE historical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT, identity_hash TEXT NOT NULL UNIQUE,
            pauta_transmision TEXT, estado TEXT, tiempo_fiscal TEXT, canal_base TEXT, orden TEXT, fecha TEXT,
            dependencia_cam_sen TEXT, clave TEXT, campana TEXT, version TEXT,
            source_batch_id TEXT NOT NULL REFERENCES import_batches(batch_id), source_filename TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        c.execute("INSERT INTO import_batches VALUES ('B-001','2026-08-01T00:00:00Z','PROCESADO')")
        c.execute("""INSERT INTO historical_records(identity_hash,pauta_transmision,estado,tiempo_fiscal,canal_base,orden,fecha,dependencia_cam_sen,clave,campana,version,source_batch_id,source_filename) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", ('h','P-1','ACTIVO','00:30','1','1','2026-08-01','CAM. SEN.','K1','Campaña X','V1','B-001','a.xlsx'))
        c.execute("""INSERT INTO historical_records(identity_hash,pauta_transmision,estado,tiempo_fiscal,canal_base,orden,fecha,dependencia_cam_sen,clave,campana,version,source_batch_id,source_filename) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", ('h2','P-2','INACTIVO','00:30','2','2','2026-08-02','CAM. SEN.','K2','Campaña Y','V2','B-001','b.xlsx'))


def test_search_filters_and_paginates(tmp_path: Path) -> None:
    db = tmp_path / 'db.sqlite'
    setup_db(db)
    service = HistoricalQueryService(HistoricalRepository(db))
    result = service.search(HistoricalQueryFilters(estado='ACTIVO', limit=1))
    assert result.total == 1
    assert len(result.records) == 1
    assert result.records[0]['clave'] == 'K1'


def test_invalid_sort_column_is_rejected(tmp_path: Path) -> None:
    db = tmp_path / 'db.sqlite'
    setup_db(db)
    service = HistoricalQueryService(HistoricalRepository(db))
    try:
        service.search(HistoricalQueryFilters(sort_by='drop table'))
    except ValueError as exc:
        assert 'no permitido' in str(exc)
    else:
        raise AssertionError('se esperaba ValueError')
