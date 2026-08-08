from datetime import date, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.infrastructure.orm import Base, RtcRecordModel


def test_schema_creates_on_sqlite() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    assert "rtc_record" in Base.metadata.tables
    assert "source_file" in Base.metadata.tables
    assert "import_batch" in Base.metadata.tables


def test_rtc_business_key_is_unique() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    values = dict(
        batch_id="batch-1", pauta_transmision="P", estado="E", tiempo_fiscal="TF",
        canal_base="C", orden="O", fecha=date(2026, 8, 1), dependencia="CAM. SEN.",
        clave="K", campana="Campaña", version="Versión",
    )
    with Session(engine) as session:
        session.add(RtcRecordModel(**values))
        session.commit()
        session.add(RtcRecordModel(**values))
        with pytest.raises(IntegrityError):
            session.commit()
