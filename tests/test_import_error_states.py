from pathlib import Path
import sqlite3
import pytest

from app.infrastructure.import_transaction import ImportTransaction


def setup(path: Path) -> None:
    with sqlite3.connect(path) as c:
        c.executescript('''
        CREATE TABLE import_batches (batch_id TEXT PRIMARY KEY, started_at TEXT NOT NULL, status TEXT NOT NULL);
        CREATE TABLE historical_records (id INTEGER PRIMARY KEY, identity_hash TEXT UNIQUE, source_batch_id TEXT REFERENCES import_batches(batch_id), source_filename TEXT);
        CREATE TABLE duplicate_audit (id INTEGER PRIMARY KEY, identity_hash TEXT, batch_id TEXT REFERENCES import_batches(batch_id), source_filename TEXT, existing_record_id INTEGER, detected_at TEXT DEFAULT CURRENT_TIMESTAMP, UNIQUE(identity_hash,batch_id,source_filename));
        ''')


def test_failed_transaction_does_not_leave_processed_batch(tmp_path: Path) -> None:
    db = tmp_path / 'db.sqlite'
    setup(db)
    tx = ImportTransaction(db)
    with pytest.raises(sqlite3.OperationalError):
        with tx.begin('B-ERR') as c:
            c.execute('INSERT INTO historical_records(identity_hash, source_batch_id, source_filename) VALUES (?, ?, ?)', ('h', 'B-ERR', 'x.xlsx'))
            c.execute('INSERT INTO table_that_does_not_exist VALUES (1)')
    with sqlite3.connect(db) as c:
        assert c.execute("SELECT COUNT(*) FROM import_batches WHERE batch_id='B-ERR'").fetchone()[0] == 0
        assert c.execute('SELECT COUNT(*) FROM historical_records').fetchone()[0] == 0
