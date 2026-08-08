from pathlib import Path
import sqlite3

from openpyxl import Workbook

from app.application.import_orchestrator import ImportOrchestrator
from app.processing.cam_sen_filter import CamSenFilter
from app.processing.rtc_reader import RTCExcelReader


def create_schema(path: Path) -> None:
    with sqlite3.connect(path) as connection:
        connection.executescript(
            """
            CREATE TABLE import_batches (
                batch_id TEXT PRIMARY KEY,
                started_at TEXT NOT NULL,
                status TEXT NOT NULL
            );
            CREATE TABLE historical_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identity_hash TEXT NOT NULL UNIQUE,
                pauta_transmision TEXT, estado TEXT, tiempo_fiscal TEXT,
                canal_base TEXT, orden TEXT, fecha TEXT,
                dependencia_cam_sen TEXT, clave TEXT, campana TEXT, version TEXT,
                source_batch_id TEXT NOT NULL REFERENCES import_batches(batch_id),
                source_filename TEXT NOT NULL
            );
            CREATE TABLE duplicate_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identity_hash TEXT NOT NULL,
                batch_id TEXT NOT NULL REFERENCES import_batches(batch_id),
                source_filename TEXT NOT NULL,
                existing_record_id INTEGER,
                detected_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(identity_hash, batch_id, source_filename)
            );
            """
        )


def create_workbook(path: Path) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Pauta"
    sheet.append([
        "Pauta de transmisión", "Estado", "Tiempo Fiscal", "Canal Base",
        "Orden", "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión"
    ])
    sheet.append([
        "P-001", "ACTIVO", "00:30", "1", "10", "2026-08-01",
        "CAM. SEN.", "CL-01", "Campaña X", "V1"
    ])
    sheet.append([
        "P-002", "ACTIVO", "00:30", "1", "11", "2026-08-01",
        "OTRA DEPENDENCIA", "CL-02", "Campaña Y", "V1"
    ])
    workbook.save(path)
    workbook.close()


class AlwaysValid:
    def validate(self, path: Path):
        class Result:
            valid = True
            error = None
            sha256 = "fixture"
            def __init__(self, path): self.path = path
        return Result(path)


def test_pipeline_persists_only_cam_sen(tmp_path: Path) -> None:
    db = tmp_path / "siap.sqlite"
    workbook = tmp_path / "rtc.xlsx"
    create_schema(db)
    create_workbook(workbook)

    orchestrator = ImportOrchestrator(
        database_path=db,
        validator=AlwaysValid(),
        reader=RTCExcelReader(),
        cam_sen_filter=CamSenFilter(),
    )
    result = orchestrator.process([workbook], "B-001")

    assert result.status == "PROCESADO"
    assert result.files[0].records_read == 2
    assert result.files[0].cam_sen_records == 1
    assert result.files[0].rejected == 1

    with sqlite3.connect(db) as connection:
        assert connection.execute("SELECT COUNT(*) FROM historical_records").fetchone()[0] == 1
        assert connection.execute("SELECT status FROM import_batches WHERE batch_id='B-001'").fetchone()[0] == "PROCESADO"
