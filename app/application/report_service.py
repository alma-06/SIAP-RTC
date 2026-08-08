"""Application service for filtered executive RTC reports."""

from __future__ import annotations

from pathlib import Path
from sqlalchemy.orm import Session

from app.application.export import RtcExcelExporter
from app.application.queries import RtcQueryService


class RtcReportService:
    """Query historical records and export them as an executive workbook."""

    def __init__(self, session: Session, exporter: RtcExcelExporter | None = None) -> None:
        self._session = session
        self._exporter = exporter or RtcExcelExporter()

    def export(self, output: Path, **filters: object) -> Path:
        records = RtcQueryService(self._session).list_records(**filters)
        if not records:
            raise ValueError("La consulta no contiene registros para exportar")
        return self._exporter.export(records, output)
