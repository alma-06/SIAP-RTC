"""Operational dashboard widgets for the SIAP-RTC desktop client."""

from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget


class IndicatorCard(QGroupBox):
    """Simple reusable indicator card."""

    def __init__(self, title: str, value: str = "0") -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel(title)
        value_label = QLabel(value)
        value_label.setObjectName("indicatorValue")
        layout.addWidget(label)
        layout.addWidget(value_label)
        self.value_label = value_label

    def set_value(self, value: object) -> None:
        self.value_label.setText(str(value))


class DashboardWidget(QWidget):
    """Executive overview of the historical RTC dataset."""

    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout(self)
        self.spots = IndicatorCard("Spots")
        self.campaigns = IndicatorCard("Campañas")
        self.versions = IndicatorCard("Versiones")
        self.channels = IndicatorCard("Canales")
        self.states = IndicatorCard("Estados")
        cards = [self.spots, self.campaigns, self.versions, self.channels, self.states]
        for index, card in enumerate(cards):
            layout.addWidget(card, 0, index)
        self.status = QLabel("Sin consulta ejecutada.")
        layout.addWidget(self.status, 1, 0, 1, 5)

    def update_indicators(self, indicators: object) -> None:
        self.spots.set_value(indicators.total_spots)
        self.campaigns.set_value(indicators.campaigns)
        self.versions.set_value(indicators.versions)
        self.channels.set_value(indicators.channels)
        self.states.set_value(indicators.states)
        self.status.setText("Indicadores actualizados.")
