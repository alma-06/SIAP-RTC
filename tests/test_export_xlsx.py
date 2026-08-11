from openpyxl import load_workbook

from app.export.contracts import build_export_payload
from app.export.xlsx import export_xlsx
from app.dashboard.fact_sheet import build_fact_sheet
from app.dashboard.model import DashboardPeriod


def test_export_xlsx_creates_executive_summary(tmp_path) -> None:
    period = DashboardPeriod("2026-Q2", 100, 10, 5, 80, 5, 0.80, 0.05, 0.10, 0.05, True, (), "EV-01")
    payload = build_export_payload(build_fact_sheet(period))
    output = export_xlsx(payload, tmp_path / "siap_rtc.xlsx")
    workbook = load_workbook(output, read_only=True, data_only=True)
    sheet = workbook["Resumen ejecutivo"]
    assert sheet["A1"].value == "SIAP-RTC"
    assert sheet["B4"].value == "2026-Q2"
    assert sheet["A8"].value == "Total comparado"
    assert sheet["B8"].value == 100
