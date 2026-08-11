from openpyxl import Workbook

from app.validation.rtc_preflight import validate_rtc_workbook

HEADERS = ["Pauta de transmisión", "Estado", "Tiempo Fiscal", "Canal Base", "Orden", "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión"]


def test_preflight_counts_senate_rows_and_blank_rows(tmp_path) -> None:
    source = tmp_path / "rtc.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(HEADERS)
    sheet.append(["Pauta", "Programada", "00:00:30", "AM", "O1", "11/08/2026", "CAM. SEN.", "C1", "Campaña", "V1"])
    sheet.append(["Pauta", "Programada", "00:00:30", "AM", "O2", "11/08/2026", "Otra dependencia", "C2", "Campaña", "V2"])
    sheet.append([None] * len(HEADERS))
    workbook.save(source)

    validation = validate_rtc_workbook(source)
    assert validation.valid
    assert validation.sheets[0].data_rows == 2
    assert validation.sheets[0].senate_rows == 1
    assert validation.sheets[0].blank_rows == 1


def test_preflight_reports_missing_columns(tmp_path) -> None:
    source = tmp_path / "bad.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Fecha", "Orden"])
    sheet.append(["11/08/2026", "O1"])
    workbook.save(source)

    validation = validate_rtc_workbook(source)
    assert not validation.valid
    assert "Pauta de transmisión" in validation.sheets[0].missing_columns
