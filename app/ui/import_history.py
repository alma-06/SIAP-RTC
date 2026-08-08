"""Desktop view for SIAP-RTC import history."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class ImportHistoryWidget(QWidget):
    """Display auditable import batches and their outcomes."""

    batch_selected = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Lote", "Inicio", "Fin", "Importados", "Rechazados", "Duplicados",
        ])
        self.table.setSortingEnabled(True)
        self.table.cellDoubleClicked.connect(self._select_batch)
        layout.addWidget(self.table)

    def set_batches(self, batches: list[object]) -> None:
        self.table.setRowCount(0)
        for batch in batches:
            row = self.table.rowCount()
            self.table.insertRow(row)
            values = [
                batch.id, batch.started_at, batch.finished_at,
                batch.imported_count, batch.rejected_count, batch.duplicate_count,
            ]
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))

    def _select_batch(self, row: int, _column: int) -> None:
        item = self.table.item(row, 0)
        if item:
            self.batch_selected.emit(item.text())
