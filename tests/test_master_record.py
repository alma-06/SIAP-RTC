from app.validation.master_record import MasterRecord


def test_master_record_round_trip(tmp_path) -> None:
    record = MasterRecord(
        period="2026-Q2",
        version="SIAP-RTC v0.1.0-rc1",
        run_id="RC1-001",
        source_files=("pauta.xlsx",),
        source_sha256=("abc123",),
        rules=("CAM-SEN",),
        technical_opinion="NO_VALIDADO",
    )
    path = tmp_path / "master.json"
    record.save(path)
    assert MasterRecord.load(path) == record
