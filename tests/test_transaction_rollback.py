from pathlib import Path
import sqlite3
import pytest

from app.infrastructure.import_transaction import ImportTransaction


def setup_db(path: Path) -> None:
    with sqlite3.connect(path) as c:
        c.executescript('''
        CREATE TABLE import_batches (batch_id TEXT PRIMARY KEY, started_at TEXT NOT NULL, status TEXT NOT NULL);
        CREATE TABLE historical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT, identity_hash TEXT NOT NULL UNIQUE,
            pauta_transmision TEXT, estado TEXT, tiempo_fiscal TEXT, canal_base TEXT, orden TEXT, fecha TEXT,
            dependencia_cam_sen TEXT, clave TEXT, campana TEXT, version TEXT,
            source_batch_id TEXT NOT NULL REFERENCES import_batches(batch_id), source_filename TEXT NOT NULL
        );
        CREATE TABLE duplicate_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT, identity_hash TEXT NOT NULL,
            batch_id TEXT NOT NULL REFERENCES import_batches(batch_id), source_filename TEXT NOT NULL,
            existing_record_id INTEGER, detected_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(identity_hash, batch_id, source_filename)
        );
        ''')


def record(key: str):
    return {'pauta_transmision':key,'estado':'A','tiempo_fiscal':'00:30','canal_base':'1','orden':'1',
            'fecha':'2026-08-01','dependencia_cam_sen':'CAM. SEN.','clave':key,'campana':'C','version':'V1'}


def test_failure_rolls_back_batch_and_records(tmp_path: Path) -> None:
    db = tmp_path / 'db.sqlite'
    setup_db(db)
    tx = ImportTransaction(db)
    with pytest.raises(RuntimeError):
        with tx.begin('B-FAIL') as c:
            assert tx.insert_record_or_audit_duplicate(c, record('A'), batch_id='B-FAIL', source_filename='a.xlsx') is True
            raise RuntimeError('simulated persistence failure')
    with sqlite3.connect(db) as c:
        assert c.execute("SELECT COUNT(*) FROM import_batches WHERE batch_id='B-FAIL'").fetchone()[0] == 0
        assert c.execute('SELECT COUNT(*) FROM historical_records').fetchone()[0] == 0
        assert c.execute('SELECT COUNT(*) FROM duplicate_audit').fetchone()[0] == 0
