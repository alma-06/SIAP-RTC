from openpyxl import Workbook

from app.pipeline.rtc_ingest import ingest_rtc_workbooks


def test_ingest_reads_multiple_sheets_and_filters_cam_sen(tmp_path) -> None:
    path = tmp_path / "rtc.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Pauta"
    headers = [
        "Pauta de transmisión", "Estado", "Tiempo Fiscal", "Canal Base", "Orden",
        "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión",
    ]
    sheet.append(headers)
    sheet.append(["P1", "Programada", "30", "AM", "O1", "2026-01-01", "CAM. SEN.", "C1", "Campaña", "V1"])
    sheet.append(["P2", "Programada", "30", "AM", "O2", "2026-01-01", "OTRA", "C2", "Campaña", "V1"])
    workbook.save(path)

    result = ingest_rtc_workbooks([path])
    assert len(result.records) == 1
    assert result.records[0].values["Orden"] == "O1"
    assert result.warnings == ()
