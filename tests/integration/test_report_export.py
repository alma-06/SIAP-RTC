from datetime import date
from pathlib import Path

from openpyxl import load_workbook
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.application.report_service import RtcReportService
from app.infrastructure.orm import Base, RtcRecordModel


def test_report_export_writes_expected_workbook(tmp_path: Path) -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(RtcRecordModel(
            id="r1", batch_id="b1", pauta_transmision="P1", estado="VIGENTE",
            tiempo_fiscal="FISCAL", canal_base="CANAL", orden="O1", fecha=date(2026, 8, 1),
            dependencia="CAM. SEN.", clave="K1", campana="Campaña 1", version="V1",
        ))
        session.commit()
        output = tmp_path / "reporte.xlsx"
        RtcReportService(session).export(output)
    workbook = load_workbook(output)
    assert workbook["Base consolidada"]["G2"].value == "CAM. SEN."
    assert workbook["Resumen ejecutivo"]["B2"].value == 1
