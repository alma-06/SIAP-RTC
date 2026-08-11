from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from app.dashboard.fact_sheet import ExecutiveFactSheet


class ExportFormat(str, Enum):
    XLSX = "xlsx"
    DOCX = "docx"
    PPTX = "pptx"


@dataclass(frozen=True)
class ExportPayload:
    title: str
    subtitle: str
    period: str
    status: str
    metrics: Mapping[str, int | float | str]
    alerts: tuple[str, ...]
    evidence_id: str


def build_export_payload(sheet: ExecutiveFactSheet, title: str = "SIAP-RTC") -> ExportPayload:
    kpis = sheet.kpis
    return ExportPayload(
        title=title,
        subtitle="Ficha ejecutiva de conciliación",
        period=kpis.period,
        status=sheet.status_label,
        metrics={
            "Total comparado": kpis.total_compared,
            "Adiciones": kpis.additions,
            "Modificaciones": kpis.modifications,
            "Permanencias": kpis.persistence,
            "Remociones / ausencias": kpis.removals,
            "Tasa de coincidencia": kpis.match_rate,
            "Tasa de cambio": kpis.change_rate,
        },
        alerts=tuple(alert.message for alert in sheet.alerts),
        evidence_id=kpis.evidence_id,
    )
