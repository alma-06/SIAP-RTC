from pathlib import Path

import pandas as pd

from app.application.rtc_import import RtcImportPipeline


class FakeSheet:
    name = "Pauta"
    frame = pd.DataFrame(
        [
            ["P1", "Vigente", "Fiscal", "Canal 1", "O1", "2026-08-01", "CAM. SEN.", "K1", "C1", "V1"],
            ["P1", "Vigente", "Fiscal", "Canal 1", "O1", "2026-08-01", "CAM SEN", "K1", "C1", "V1"],
            ["P2", "Vigente", "Fiscal", "Canal 2", "O2", "2026-08-01", "OTRA DEPENDENCIA", "K2", "C2", "V2"],
        ],
        columns=["Pauta de transmisión", "Estado", "Tiempo Fiscal", "Canal Base", "Orden", "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión"],
    )


class FakeReader:
    def read(self, path: Path):
        return [FakeSheet()]


def test_pipeline_filters_senate_and_deduplicates(tmp_path: Path) -> None:
    source = tmp_path / "rtc.xlsx"
    source.write_bytes(b"test")
    result = RtcImportPipeline(FakeReader()).run([source])
    assert result.rows_read == 3
    assert len(result.accepted) == 1
    assert result.duplicates == 1
    assert result.rejected == 0
    assert result.accepted[0].dependencia == "CAM. SEN."
    assert len(result.file_hashes[source]) == 64
