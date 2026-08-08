"""End-to-end import facade used by the desktop application."""

from __future__ import annotations

from pathlib import Path

from app.application.import_report import ImportReport
from app.application.rtc_import_service import RtcImportService


class EndToEndImportService:
    """Single application entry point for GUI-driven RTC imports."""

    def __init__(self, service: RtcImportService) -> None:
        self._service = service

    def execute(self, files: list[Path]) -> ImportReport:
        if not files:
            raise ValueError("Debe seleccionarse al menos un archivo RTC")
        result = self._service.execute(files)
        return ImportReport.from_result(result)
