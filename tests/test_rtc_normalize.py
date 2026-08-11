from datetime import date

from app.pipeline.normalize import normalize_date, normalize_records, normalize_time
from app.pipeline.rtc_ingest import IngestedRecord


def test_normalize_date_and_time() -> None:
    assert normalize_date(date(2026, 8, 11)) == "2026-08-11"
    assert normalize_date("11/08/2026") == "2026-08-11"
    assert normalize_time("00:00:30") == 30
    assert normalize_time("1:02") == 3720


def test_normalize_record_canonicalizes_text_and_flags_empty_fields() -> None:
    record = IngestedRecord("rtc.xlsx", {
        "Pauta de transmisión": "  PAUTA   A ",
        "Estado": " Programada ",
        "Tiempo Fiscal": "00:00:30",
        "Canal Base": " AM ",
        "Orden": " O-1 ",
        "Fecha": "11/08/2026",
        "Dependencia CAM. SEN.": " CAM. SEN. ",
        "Clave": " C-1 ",
        "Campaña": " Campaña ",
        "Versión": " V1 ",
    })
    result = normalize_records([record])
    assert result.records[0].values["Pauta de transmisión"] == "pauta a"
    assert result.records[0].values["Tiempo Fiscal"] == 30
    assert result.records[0].values["Fecha"] == "2026-08-11"
    assert result.warnings == ()
