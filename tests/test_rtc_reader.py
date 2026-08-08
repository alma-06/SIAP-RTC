from pathlib import Path

from openpyxl import Workbook

from app.processing.rtc_reader import RTCExcelReader


def create_fixture(path: Path) -> None:
    workbook = Workbook()
    first = workbook.active
    first.title = "Pauta"
    first.append([
        "Pauta de Transmisión", "ESTADO", "Tiempo Fiscal", "Canal Base",
        "Orden", "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión"
    ])
    first.append([
        "P-001", "ACTIVO", "00:30", "1", "10", "2026-08-01",
        "Cám. Sen.", "CL-01", "Campaña X", "V1"
    ])
    first.append([None] * 10)

    second = workbook.create_sheet("Otra")
    second.append(["Dependencia CAM SEN", "Clave"])
    second.append(["OTRA DEPENDENCIA", "X"])
    workbook.save(path)
    workbook.close()


def test_reader_normalizes_headers_and_preserves_origin(tmp_path: Path) -> None:
    path = tmp_path / "rtc_fixture.xlsx"
    create_fixture(path)
    records = RTCExcelReader().read(path)

    assert len(records) == 2
    assert records[0].source_sheet == "Pauta"
    assert records[0].source_row == 2
    assert records[0].values["dependencia_cam_sen"] == "Cám. Sen."
    assert records[1].source_sheet == "Otra"
    assert records[1].source_row == 2
