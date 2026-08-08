"""Audit detail dialog for SIAP-RTC import batches."""

from __future__ import annotations

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLabel, QListWidget, QVBoxLayout

from app.application.audit import BatchAuditDetail


class AuditDetailDialog(QDialog):
    """Display source, integrity and persistence information for a batch."""

    def __init__(self, detail: BatchAuditDetail) -> None:
        super().__init__()
        self.setWindowTitle(f"Auditoría del lote {detail.batch_id}")
        self.resize(820, 560)
        root = QVBoxLayout(self)
        form = QFormLayout()
        values = [
            ("Lote", detail.batch_id),
            ("Inicio", detail.started_at),
            ("Fin", detail.finished_at or "En ejecución"),
            ("Importados", detail.imported_count),
            ("Rechazados", detail.rejected_count),
            ("Duplicados", detail.duplicate_count),
            ("Registros persistidos", detail.persisted_records),
        ]
        for label, value in values:
            form.addRow(QLabel(label), QLabel(str(value)))
        root.addLayout(form)
        root.addWidget(QLabel("Archivos fuente y SHA-256"))
        sources = QListWidget()
        sources.addItems([f"{path} | SHA-256: {sha}" for path, sha in zip(detail.source_files, detail.source_hashes)])
        root.addWidget(sources)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        root.addWidget(buttons)
