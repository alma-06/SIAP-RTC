"""Presentation DTO for import execution results."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.application.rtc_import import ImportResult


@dataclass(frozen=True, slots=True)
class ImportReport:
    files: int
    rows_read: int
    accepted: int
    duplicates: int
    rejected: int
    issues: tuple[str, ...]
    source_files: tuple[str, ...]

    @classmethod
    def from_result(cls, result: ImportResult) -> "ImportReport":
        return cls(
            files=result.files_processed,
            rows_read=result.rows_read,
            accepted=len(result.accepted),
            duplicates=result.duplicates,
            rejected=result.rejected,
            issues=tuple(
                f"{issue.file.name} | {issue.sheet} | fila {issue.row or '-'} | {issue.message}"
                for issue in result.issues
            ),
            source_files=tuple(str(path) for path in result.file_hashes),
        )
