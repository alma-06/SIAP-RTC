from openpyxl import Workbook

from app.pipeline.integrated import run_integrated_period


HEADERS = [
    "Pauta de transmisión", "Estado", "Tiempo Fiscal", "Canal Base", "Orden",
    "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión",
]


def make_workbook(path, order: str) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(HEADERS)
    sheet.append(["Pauta", "Programada", "00:00:30", "AM", order, "11/08/2026", "CAM. SEN.", "C1", "Campaña", "V1"])
    workbook.save(path)


def test_integrated_period_runs_ingestion_to_evidence(tmp_path) -> None:
    source = tmp_path / "rtc.xlsx"
    make_workbook(source, "O1")
    result = run_integrated_period([source], "2026-Q2")
    assert len(result.ingestion.records) == 1
    assert len(result.deduplication.records) == 1
    assert len(result.consolidation.records) == 1
    assert result.reconciliation is None
    assert result.indicators is None
    assert result.evidence.evidence_id == "EV-2026-Q2"
    assert result.evidence.sources[0].filename == "rtc.xlsx"


def test_integrated_period_reconciles_against_previous_period(tmp_path) -> None:
    previous_file = tmp_path / "previous.xlsx"
    current_file = tmp_path / "current.xlsx"
    make_workbook(previous_file, "O1")
    make_workbook(current_file, "O2")
    previous = run_integrated_period([previous_file], "2026-Q1")
    current = run_integrated_period([current_file], "2026-Q2", previous=previous.consolidation)
    assert current.reconciliation is not None
    assert current.indicators is not None
    assert current.indicators.added_count == 1
    assert current.indicators.removed_count == 1
