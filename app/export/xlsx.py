from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

from app.export.contracts import ExportPayload


def export_xlsx(payload: ExportPayload, output_path: str | Path) -> Path:
    path = Path(output_path)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Resumen ejecutivo"

    sheet["A1"] = payload.title
    sheet["A1"].font = Font(bold=True, size=16)
    sheet["A2"] = payload.subtitle
    sheet["A4"] = "Periodo"
    sheet["B4"] = payload.period
    sheet["A5"] = "Estado"
    sheet["B5"] = payload.status
    sheet["A7"] = "Indicador"
    sheet["B7"] = "Valor"
    sheet["A7"].font = Font(bold=True)
    sheet["B7"].font = Font(bold=True)

    row = 8
    for label, value in payload.metrics.items():
        sheet.cell(row=row, column=1, value=label)
        sheet.cell(row=row, column=2, value=value)
        row += 1

    row += 1
    sheet.cell(row=row, column=1, value="Alertas")
    sheet.cell(row=row, column=1).font = Font(bold=True)
    row += 1
    if payload.alerts:
        for alert in payload.alerts:
            sheet.cell(row=row, column=1, value=alert)
            row += 1
    else:
        sheet.cell(row=row, column=1, value="Sin alertas")
        row += 1

    row += 1
    sheet.cell(row=row, column=1, value="Evidencia")
    sheet.cell(row=row, column=2, value=payload.evidence_id)

    sheet.column_dimensions["A"].width = 32
    sheet.column_dimensions["B"].width = 24
    workbook.save(path)
    return path
