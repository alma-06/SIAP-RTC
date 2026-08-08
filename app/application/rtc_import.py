"""Application pipeline for reading, validating and filtering RTC workbooks."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from app.application.rtc_normalizer import homologate_headers, normalize_dependency
from app.domain.rtc import RtcRecord
from app.infrastructure.excel_reader import ExcelReader

REQUIRED_FIELDS = {
    "pauta_transmision", "estado", "tiempo_fiscal", "canal_base", "orden",
    "fecha", "dependencia", "clave", "campana", "version",
}


@dataclass(slots=True)
class ImportIssue:
    """A non-fatal issue associated with a source workbook row."""

    file: Path
    sheet: str
    row: int | None
    message: str


@dataclass(slots=True)
class ImportResult:
    """Deterministic result of an RTC import execution."""

    files_processed: int = 0
    rows_read: int = 0
    accepted: list[RtcRecord] = field(default_factory=list)
    duplicates: int = 0
    rejected: int = 0
    issues: list[ImportIssue] = field(default_factory=list)
    file_hashes: dict[Path, str] = field(default_factory=dict)


class RtcImportPipeline:
    """Read RTC Excel files and produce validated Senate records."""

    def __init__(self, reader: ExcelReader | None = None) -> None:
        self._reader = reader or ExcelReader()

    def run(self, files: list[Path]) -> ImportResult:
        result = ImportResult()
        seen: set[tuple[str, ...]] = set()
        for path in files:
            if not path.exists():
                result.issues.append(ImportIssue(path, "", None, "Archivo no encontrado"))
                continue
            result.files_processed += 1
            result.file_hashes[path] = self._sha256(path)
            for sheet in self._reader.read(path):
                mapping = homologate_headers(list(sheet.frame.columns))
                if not REQUIRED_FIELDS.issubset(mapping.values()):
                    result.issues.append(
                        ImportIssue(path, sheet.name, None, "Faltan columnas obligatorias")
                    )
                    continue
                frame = sheet.frame.rename(columns=mapping)
                for index, row in frame.iterrows():
                    result.rows_read += 1
                    try:
                        record = self._to_record(row, int(index) + 2)
                    except (TypeError, ValueError, KeyError) as exc:
                        result.rejected += 1
                        result.issues.append(
                            ImportIssue(path, sheet.name, int(index) + 2, str(exc))
                        )
                        continue
                    if not record.is_senate_record:
                        continue
                    key = record.business_key.normalized()
                    if key in seen:
                        result.duplicates += 1
                        continue
                    seen.add(key)
                    result.accepted.append(record)
        return result

    @staticmethod
    def _to_record(row: Any, source_row_number: int) -> RtcRecord:
        raw_date = row["fecha"]
        parsed_date = pd.to_datetime(raw_date, errors="raise").date()
        if not isinstance(parsed_date, date):
            raise ValueError("Fecha inválida")
        dependency = normalize_dependency(row["dependencia"])
        return RtcRecord(
            pauta_transmision=str(row["pauta_transmision"]).strip(),
            estado=str(row["estado"]).strip(),
            tiempo_fiscal=str(row["tiempo_fiscal"]).strip(),
            canal_base=str(row["canal_base"]).strip(),
            orden=str(row["orden"]).strip(),
            fecha=parsed_date,
            dependencia=dependency,
            clave=str(row["clave"]).strip(),
            campana=str(row["campana"]).strip(),
            version=str(row["version"]).strip(),
            source_row_number=source_row_number,
        )

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
