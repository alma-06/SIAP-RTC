"""Import result summary dialog."""

from __future__ import annotations

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLabel, QListWidget, QVBoxLayout

from app.application.import_report import ImportReport


class ImportSummaryDialog(QDialog):
    """Display an auditable summary after an RTC import."""

    def __init__(self, report: ImportReport) -> None:
        super().__init__()
        self.setWindowTitle("Resultado de importación | SIAP-RTC")
        self.resize(720, 480)
        root = QVBoxLayout(self)
        form = QFormLayout()
        values = (
            ("Archivos procesados", report.files),
            ("Filas leídas", report.rows_read),
            ("Registros aceptados", report.accepted),
            ("Duplicados", report.duplicates),
            ("Rechazados", report.rejected),
        )
        for label, value in values:
            form.addRow(QLabel(label), QLabel(str(value)))
        root.addLayout(form)
        root.addWidget(QLabel("Incidencias"))
        issues = QListWidget()
        issues.addItems(report.issues or ["Sin incidencias."])
        root.addWidget(issues)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        root.addWidget(buttons)
