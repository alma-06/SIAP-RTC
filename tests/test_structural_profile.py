from openpyxl import Workbook

from app.validation.structural_profile import profile_workbook

HEADERS = ["Pauta de transmisión", "Estado", "Tiempo Fiscal", "Canal Base", "Orden", "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión"]


def test_profile_collects_structural_and_sample_data(tmp_path) -> None:
    source = tmp_path / "rtc.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Semana 1"
    sheet.append(HEADERS)
    sheet.append(["Pauta", "Programada", "00:00:30", "AM", "O1", "11/08/2026", "CAM. SEN.", "C1", "Campaña", "V1"])
    sheet.append([None] * len(HEADERS))
    workbook.save(source)

    profile = profile_workbook(source)
    sheet_profile = profile.sheets[0]
    assert profile.sheet_count == 1
    assert len(profile.sha256) == 64
    assert sheet_profile.data_rows == 1
    assert sheet_profile.senate_rows == 1
    assert sheet_profile.blank_rows == 1
    assert "11/08/2026" in sheet_profile.date_values
    assert "00:00:30" in sheet_profile.time_fiscal_samples
