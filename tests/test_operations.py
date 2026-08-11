from openpyxl import Workbook

from app.ui.operations import OperationRequest, execute_operation

HEADERS = ["Pauta de transmisión", "Estado", "Tiempo Fiscal", "Canal Base", "Orden", "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión"]


def test_operation_stops_before_pipeline_when_preflight_fails(tmp_path) -> None:
    source = tmp_path / "bad.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Fecha", "Orden"])
    sheet.append(["11/08/2026", "O1"])
    workbook.save(source)

    response = execute_operation(OperationRequest((source,), "2026-Q2"))
    assert response.result is None
    assert not response.preflight[0].valid


def test_operation_runs_pipeline_after_successful_preflight(tmp_path) -> None:
    source = tmp_path / "rtc.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(HEADERS)
    sheet.append(["Pauta", "Programada", "00:00:30", "AM", "O1", "11/08/2026", "CAM. SEN.", "C1", "Campaña", "V1"])
    workbook.save(source)

    response = execute_operation(OperationRequest((source,), "2026-Q2"))
    assert response.result is not None
    assert response.preflight[0].valid
