from datetime import datetime, timezone
from pathlib import Path

from app.domain.entities import ImportBatch, RtcSourceFile
from app.domain.rtc import RtcRecord
from app.domain.value_objects import FileHash
from app.infrastructure.rtc_persistence import RtcPersistence


def test_persist_batch_writes_source_batch_and_record(tmp_path: Path) -> None:
    database = tmp_path / "siap.db"
    persistence = RtcPersistence(f"sqlite:///{database}")
    now = datetime(2026, 8, 1, tzinfo=timezone.utc)
    source = RtcSourceFile(Path("rtc.xlsx"), FileHash("a" * 64), now)
    batch = ImportBatch([source.id], now, imported_count=1)
    batch.finish(now)
    record = RtcRecord(
        "P1", "VIGENTE", "FISCAL", "CANAL", "O1", now.date(),
        "CAM. SEN.", "K1", "C1", "V1", 2,
    )
    persistence.persist_batch(batch, [source], [record])
    with persistence.engine.connect() as connection:
        assert connection.exec_driver_sql("SELECT COUNT(*) FROM source_file").scalar_one() == 1
        assert connection.exec_driver_sql("SELECT COUNT(*) FROM import_batch").scalar_one() == 1
        assert connection.exec_driver_sql("SELECT COUNT(*) FROM rtc_record").scalar_one() == 1
