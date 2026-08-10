from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.methodology.conciliation_case import ConciliationCase


@dataclass(frozen=True)
class ExcelConciliationWorkbook:
    """Specification/data model for the institutional XLSX export."""

    case: ConciliationCase

    def sheets(self) -> dict[str, list[tuple[str, object]]]:
        evidence = self.case.evidence_summary()
        result = self.case.calculate()
        return {
            "Resumen": [
                ("Caso", self.case.case_id),
                ("Periodo", self.case.period),
                ("Resultado [h]:mm:ss]", result.elapsed_time),
                ("Segundos", result.total_seconds),
                ("Interpretación", result.interpretation),
            ],
            "Parámetros": [
                ("Impactos", self.case.impacts),
                ("Radiodifusoras", self.case.universe.total_stations),
                ("Duración estándar (segundos)", self.case.standard_spot_seconds),
                ("Fuente universo", self.case.universe.source),
                ("Fecha de corte", self.case.universe.cutoff_date),
                ("Metodología universo", self.case.universe.methodology),
            ],
            "Cálculo": [
                ("Fórmula", "impactos × radiodifusoras × duración estándar"),
                ("Impactos", self.case.impacts),
                ("Radiodifusoras", self.case.universe.total_stations),
                ("Duración estándar", self.case.standard_spot_seconds),
                ("Total segundos", result.total_seconds),
                ("Resultado [h]:mm:ss", result.elapsed_time),
            ],
            "Evidencia": [
                ("Archivo fuente", self.case.source_file),
                ("Hash", self.case.source_hash),
                ("Universo", self.case.universe.universe_id),
                ("Archivo universo", self.case.universe.source_file or ""),
            ],
            "Notas metodológicas": [
                ("Interpretación", result.interpretation),
                ("Notas", self.case.notes or "Sin notas adicionales."),
            ],
        }


def write_xlsx(workbook: ExcelConciliationWorkbook, output: str | Path) -> Path:
    """Write the workbook using openpyxl without embedding calculation logic."""
    from openpyxl import Workbook

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    wb.remove(wb.active)
    for sheet_name, rows in workbook.sheets().items():
        ws = wb.create_sheet(sheet_name)
        ws.append(["Campo", "Valor"])
        for label, value in rows:
            ws.append([label, value])
        ws.freeze_panes = "A2"
        ws.column_dimensions["A"].width = 34
        ws.column_dimensions["B"].width = 90
    wb.save(output_path)
    return output_path
