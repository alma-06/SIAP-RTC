from openpyxl import Workbook

from app.export.executive_package import build_executive_summary, write_executive_summary
from app.pipeline.integrated import run_integrated_period


HEADERS = [
    "Pauta de transmisión", "Estado", "Tiempo Fiscal", "Canal Base", "Orden",
    "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión",
]


def test_build_executive_summary(tmp_path) -> None:
    source = tmp_path / "rtc.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(HEADERS)
    sheet.append(["Pauta", "Programada", "00:00:30", "AM", "O1", "11/08/2026", "CAM. SEN.", "C1", "Campaña", "V1"])
    workbook.save(source)

    result = run_integrated_period([source], "2026-Q2")
    summary = build_executive_summary(result)
    assert summary["records_ingested"] == 1
    assert summary["records_kept"] == 1
    assert summary["duplicates_removed"] == 0
    assert summary["evidence_id"] == "EV-2026-Q2"

    output = tmp_path / "summary.json"
    write_executive_summary(result, output)
    assert output.exists()
