"""Desktop controls for executive RTC report generation."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QMessageBox, QPushButton, QVBoxLayout, QWidget
from sqlalchemy.orm import Session

from app.application.report_service import RtcReportService


class ReportExportWidget(QWidget):
    """Export the current historical query to an executive Excel workbook."""

    def __init__(self, session_factory) -> None:
        super().__init__()
        self._session_factory = session_factory
        self._filters: dict[str, object] = {}
        layout = QVBoxLayout(self)
        button = QPushButton("Generar reporte ejecutivo Excel")
        button.clicked.connect(self.export)
        layout.addWidget(button)

    def set_filters(self, filters: dict[str, object]) -> None:
        self._filters = dict(filters)

    def export(self) -> None:
        output, _ = QFileDialog.getSaveFileName(
            self, "Guardar reporte ejecutivo", "SIAP-RTC_reporte.xlsx", "Excel (*.xlsx)"
        )
        if not output:
            return
        try:
            with self._session_factory() as session:  # type: Session
                RtcReportService(session).export(Path(output), **self._filters)
            QMessageBox.information(self, "SIAP-RTC", f"Reporte generado correctamente:\n{output}")
        except ValueError as exc:
            QMessageBox.information(self, "SIAP-RTC", str(exc))
        except Exception as exc:
            QMessageBox.critical(self, "Error al generar reporte", str(exc))
