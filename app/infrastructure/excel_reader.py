"""Excel reader abstraction for RTC source publications."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True, slots=True)
class ExcelSheet:
    """One non-empty worksheet read from an RTC workbook."""

    name: str
    frame: pd.DataFrame


class ExcelReader:
    """Read one or more Excel workbooks without imposing business rules."""

    SUPPORTED_SUFFIXES = {".xlsx", ".xlsm"}

    def read(self, path: Path) -> list[ExcelSheet]:
        if path.suffix.lower() not in self.SUPPORTED_SUFFIXES:
            raise ValueError(f"Unsupported Excel format: {path.suffix}")
        workbook = pd.ExcelFile(path, engine="openpyxl")
        sheets: list[ExcelSheet] = []
        for name in workbook.sheet_names:
            frame = workbook.parse(name, dtype=object)
            if not frame.empty:
                sheets.append(ExcelSheet(name=name, frame=frame))
        return sheets
