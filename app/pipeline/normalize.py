from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import re
from typing import Iterable

from app.pipeline.rtc_ingest import IngestedRecord, REQUIRED_COLUMNS


@dataclass(frozen=True)
class NormalizationResult:
    records: tuple[IngestedRecord, ...]
    warnings: tuple[str, ...]


def normalize_text(value: object) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).strip()).casefold()


def normalize_date(value: object) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    text = normalize_text(value)
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return text


def normalize_time(value: object) -> int | str:
    if value is None or value == "":
        return ""
    if isinstance(value, (int, float)):
        return int(value)
    text = normalize_text(value)
    match = re.fullmatch(r"(\d+):(\d{1,2})(?::(\d{1,2}))?", text)
    if not match:
        return text
    hours = int(match.group(1))
    minutes = int(match.group(2))
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


def normalize_record(record: IngestedRecord) -> IngestedRecord:
    values = dict(record.values)
    text_columns = (
        "Pauta de transmisión", "Estado", "Canal Base", "Orden",
        "Clave", "Campaña", "Versión", "Dependencia CAM. SEN.",
    )
    for column in text_columns:
        values[column] = normalize_text(values.get(column))
    values["Fecha"] = normalize_date(values.get("Fecha"))
    values["Tiempo Fiscal"] = normalize_time(values.get("Tiempo Fiscal"))
    return IngestedRecord(record.source_file, values)


def normalize_records(records: Iterable[IngestedRecord]) -> NormalizationResult:
    normalized: list[IngestedRecord] = []
    warnings: list[str] = []
    for record in records:
        item = normalize_record(record)
        missing = [column for column in REQUIRED_COLUMNS if item.values.get(column, "") == ""]
        if missing:
            warnings.append(
                f"Registro con campos vacíos en {record.source_file}: {', '.join(missing)}"
            )
        normalized.append(item)
    return NormalizationResult(tuple(normalized), tuple(warnings))
