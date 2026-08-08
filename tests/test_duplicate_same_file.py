from pathlib import Path
import sqlite3

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


def r():
    return {'pauta_transmision':'P','estado':'A','tiempo_fiscal':'00:30','canal_base':'1','orden':'1',
            'fecha':'2026-08-01','dependencia_cam_sen':'CAM. SEN.','clave':'K','campana':'C','version':'V1'}


def test_duplicate_same_file_is_audited_once(tmp_path: Path) -> None:
    db = tmp_path / 'db.sqlite'
    setup_db(db)
    tx = ImportTransaction(db)
    with tx.begin('B-001') as c:
        assert tx.insert_record_or_audit_duplicate(c, r(), batch_id='B-001', source_filename='a.xlsx') is True
        assert tx.insert_record_or_audit_duplicate(c, r(), batch_id='B-001', source_filename='a.xlsx') is False
        assert tx.insert_record_or_audit_duplicate(c, r(), batch_id='B-001', source_filename='a.xlsx') is False
    with sqlite3.connect(db) as c:
        assert c.execute('SELECT COUNT(*) FROM historical_records').fetchone()[0] == 1
        assert c.execute('SELECT COUNT(*) FROM duplicate_audit').fetchone()[0] == 1
