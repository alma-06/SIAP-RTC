from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.application.audit import ImportAuditService
from app.infrastructure.orm import Base, ImportBatchModel, ImportBatchSourceModel, SourceFileModel, RtcRecordModel


def test_audit_detail_returns_sources_hashes_and_persisted_count() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        now = datetime(2026, 8, 7, tzinfo=timezone.utc)
        session.add(ImportBatchModel(id="b1", started_at=now, finished_at=now, imported_count=2, rejected_count=1, duplicate_count=3))
        session.add(SourceFileModel(id="s1", path="rtc.xlsx", sha256="a" * 64, received_at=now))
        session.add(ImportBatchSourceModel(batch_id="b1", source_file_id="s1"))
        session.add(RtcRecordModel(id="r1", batch_id="b1", pauta_transmision="P", estado="E", tiempo_fiscal="T", canal_base="C", orden="O", fecha=now.date(), dependencia="CAM. SEN.", clave="K", campana="C1", version="V1"))
        session.commit()
        detail = ImportAuditService(session).detail("b1")
        assert detail.persisted_records == 1
        assert detail.source_files == ("rtc.xlsx",)
        assert detail.source_hashes == ("a" * 64,)
