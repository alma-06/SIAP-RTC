from openpyxl import Workbook

from app.release.controlled_run import execute_controlled_rc1

HEADERS = ["Pauta de transmisión", "Estado", "Tiempo Fiscal", "Canal Base", "Orden", "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión"]


def test_controlled_rc1_creates_isolated_evidence(tmp_path) -> None:
    source = tmp_path / "rtc.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(HEADERS)
    sheet.append(["Pauta", "Programada", "00:00:30", "AM", "O1", "11/08/2026", "CAM. SEN.", "C1", "Campaña", "V1"])
    workbook.save(source)

    run = execute_controlled_rc1((source,), "2026-Q2", tmp_path / "runs")
    assert run.run_id.startswith("RC1-2026-Q2-")
    assert run.output_dir.exists()
    assert (run.output_dir / "EvidenceManifest.json").exists()
    assert (run.output_dir / "RunMetadata.json").exists()
    assert run.result.evidence.evidence_id.endswith("-EV")
