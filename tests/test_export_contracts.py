from app.dashboard.fact_sheet import build_fact_sheet
from app.dashboard.model import DashboardPeriod
from app.export.contracts import ExportFormat, build_export_payload


def test_export_payload_is_format_neutral() -> None:
    period = DashboardPeriod("2026-Q2", 100, 10, 5, 80, 5, 0.80, 0.05, 0.10, 0.05, True, (), "EV-01")
    payload = build_export_payload(build_fact_sheet(period))
    assert payload.period == "2026-Q2"
    assert payload.status == "COMPARABLE"
    assert payload.metrics["Total comparado"] == 100
    assert payload.evidence_id == "EV-01"
    assert {ExportFormat.XLSX.value, ExportFormat.DOCX.value, ExportFormat.PPTX.value} == {"xlsx", "docx", "pptx"}
