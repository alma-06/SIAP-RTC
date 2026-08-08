"""Generate deterministic synthetic Excel fixtures for SIAP-RTC tests."""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook

HEADERS = [
    "Pauta de transmisión", "Estado", "Tiempo Fiscal", "Canal Base", "Orden",
    "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión",
]


def write_book(path: Path, rows: list[list[object]], *, sheet: str = "Pauta") -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = sheet
    worksheet.append(HEADERS)
    for row in rows:
        worksheet.append(row)
    workbook.save(path)


def generate(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    valid = [
        ["P1", "VIGENTE", "FISCAL", "CANAL 1", "O1", "2026-08-07", "CAM. SEN.", "K1", "C1", "V1"],
        ["P2", "VIGENTE", "FISCAL", "CANAL 2", "O2", "2026-08-08", "CAM. SEN.", "K2", "C2", "V2"],
    ]
    write_book(root / "valid_single_sheet.xlsx", valid)
    write_book(root / "duplicate_rows.xlsx", valid + [valid[0]])
    write_book(root / "other_dependencies.xlsx", [valid[0][:-4] + ["OTRA DEPENDENCIA", "K3", "C3", "V3"]])
    write_book(root / "blank_rows.xlsx", [valid[0], [None] * len(HEADERS), valid[1]])
    write_book(root / "empty_workbook.xlsx", [])


if __name__ == "__main__":
    generate(Path(__file__).parent)
