from datetime import date
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.application.rtc_import import RtcImportPipeline
from app.application.rtc_import_service import RtcImportService
from app.infrastructure.orm import ImportBatchModel, RtcRecordModel
from app.infrastructure.rtc_persistence import RtcPersistence
from tests.fixtures.generate_fixtures import write_book


def test_two_weekly_imports_preserve_history_and_deduplicate(tmp_path: Path) -> None:
    week1 = tmp_path / "week1.xlsx"
    week2 = tmp_path / "week2.xlsx"
    common = ["P1", "VIGENTE", "FISCAL", "CANAL 1", "O1", "2026-08-07", "CAM. SEN.", "K1", "C1", "V1"]
    new = ["P2", "VIGENTE", "FISCAL", "CANAL 2", "O2", "2026-08-14", "CAM. SEN.", "K2", "C2", "V2"]
    write_book(week1, [common])
    write_book(week2, [common, new])

    persistence = RtcPersistence(f"sqlite:///{tmp_path / 'history.db'}")
    service = RtcImportService(RtcImportPipeline(), persistence)
    first = service.execute([week1])
    second = service.execute([week2])

    assert len(first.accepted) == 1
    assert len(second.accepted) == 1
    with Session(persistence.engine) as session:
        records = session.scalar(select(func.count(RtcRecordModel.id)))
        batches = session.scalar(select(func.count(ImportBatchModel.id)))
        assert records == 2
        assert batches == 2
