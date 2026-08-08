from pathlib import Path

from openpyxl import load_workbook
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.application.rtc_import import RtcImportPipeline
from app.application.rtc_import_service import RtcImportService
from app.infrastructure.rtc_persistence import RtcPersistence
from app.infrastructure.orm import Base, RtcRecordModel
from tests.fixtures.generate_fixtures import generate


def test_import_service_persists_fixture_records(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    generate(fixture_dir)
    db = tmp_path / "siap_rtc.db"
    persistence = RtcPersistence(f"sqlite:///{db}")
    result = RtcImportService(RtcImportPipeline(), persistence).execute([
        fixture_dir / "valid_single_sheet.xlsx",
    ])
    assert result.files_processed == 1
    assert len(result.accepted) == 2
    with Session(persistence.engine) as session:
        count = session.scalar(select(func.count(RtcRecordModel.id)))
        assert count == 2


def test_import_service_deduplicates_repeated_input(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    generate(fixture_dir)
    persistence = RtcPersistence(f"sqlite:///{tmp_path / 'siap_rtc.db'}")
    result = RtcImportService(RtcImportPipeline(), persistence).execute([
        fixture_dir / "duplicate_rows.xlsx",
    ])
    assert result.duplicates >= 1
