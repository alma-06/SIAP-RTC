from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.application.indicators import RtcIndicatorService
from app.application.queries import RtcQueryService
from app.infrastructure.orm import Base, RtcRecordModel


def test_indicators_and_queries() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for i in range(3):
            session.add(RtcRecordModel(
                batch_id="batch", pauta_transmision="P", estado="VIGENTE",
                tiempo_fiscal="FISCAL", canal_base=f"CANAL-{i % 2}", orden=f"O{i}",
                fecha=date(2026, 8, i + 1), dependencia="CAM. SEN.", clave=f"K{i}",
                campana=f"C{i % 2}", version=f"V{i % 2}",
            ))
        session.commit()
        indicators = RtcIndicatorService(session).summary()
        assert indicators.total_spots == 3
        assert indicators.campaigns == 2
        assert indicators.versions == 2
        assert indicators.channels == 2
        assert len(RtcIndicatorService(session).spots_by_date()) == 3
        assert len(RtcQueryService(session).list_records(channel="CANAL-0")) == 2
