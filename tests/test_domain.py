from datetime import date, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from app.domain.entities import ImportBatch, RtcSourceFile
from app.domain.value_objects import FileHash, RtcRecordKey


def test_file_hash_normalizes_hex() -> None:
    value = FileHash("A" * 64)
    assert value.value == "a" * 64


def test_file_hash_rejects_invalid_value() -> None:
    with pytest.raises(ValueError):
        FileHash("not-a-hash")


def test_rtc_record_key_normalizes_for_comparison() -> None:
    key = RtcRecordKey(
        " pauta ", "estado", "fiscal", "canal", "orden", date(2026, 8, 1),
        "cam. sen.", "clave", "campaña", "versión",
    )
    assert key.normalized()[0] == "PAUTA"
    assert key.normalized()[6] == "CAM. SEN."


def test_import_batch_can_finish() -> None:
    batch = ImportBatch([uuid4()], datetime(2026, 8, 1, 10, 0))
    batch.finish(datetime(2026, 8, 1, 10, 1))
    assert batch.finished_at is not None


def test_source_file_is_traceable() -> None:
    source = RtcSourceFile(
        path=Path("rtc.xlsx"),
        sha256=FileHash("b" * 64),
        received_at=datetime(2026, 8, 1, 10, 0),
    )
    assert source.id
