"""Historical query controls for SIAP-RTC."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox, QDateEdit, QFormLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget,
)
from PySide6.QtCore import QDate


class QueryPanel(QWidget):
    """Filter and display historical Senate RTC records."""

    query_requested = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        root = QVBoxLayout(self)
        form = QFormLayout()
        self.start = QDateEdit(QDate.currentDate())
        self.start.setCalendarPopup(True)
        self.end = QDateEdit(QDate.currentDate())
        self.end.setCalendarPopup(True)
        self.campaign = QComboBox()
        self.campaign.setEditable(True)
        self.campaign.setPlaceholderText("Todas")
        self.channel = QComboBox()
        self.channel.setEditable(True)
        self.channel.setPlaceholderText("Todos")
        form.addRow("Desde", self.start)
        form.addRow("Hasta", self.end)
        form.addRow("Campaña", self.campaign)
        form.addRow("Canal", self.channel)
        root.addLayout(form)
        controls = QHBoxLayout()
        search = QPushButton("Consultar")
        search.clicked.connect(self.request_query)
        clear = QPushButton("Limpiar filtros")
        clear.clicked.connect(self.clear)
        controls.addWidget(search)
        controls.addWidget(clear)
        root.addLayout(controls)
        self.table = QTableWidget(0, 10)
        self.table.setHorizontalHeaderLabels([
            "Pauta", "Estado", "Tiempo Fiscal", "Canal Base", "Orden",
            "Fecha", "Dependencia", "Clave", "Campaña", "Versión",
        ])
        self.table.setSortingEnabled(True)
        root.addWidget(self.table)

    def request_query(self) -> None:
        payload = {
            "start": self.start.date().toPython(),
            "end": self.end.date().toPython(),
            "campaign": self.campaign.currentText().strip() or None,
            "channel": self.channel.currentText().strip() or None,
        }
        self.query_requested.emit(payload)

    def clear(self) -> None:
        self.campaign.clearEditText()
        self.channel.clearEditText()
        self.table.setRowCount(0)

    def set_records(self, records: list[object]) -> None:
        self.table.setRowCount(0)
        for record in records:
            row = self.table.rowCount()
            self.table.insertRow(row)
            values = [
                record.pauta_transmision, record.estado, record.tiempo_fiscal,
                record.canal_base, record.orden, record.fecha,
                record.dependencia, record.clave, record.campana, record.version,
            ]
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))
