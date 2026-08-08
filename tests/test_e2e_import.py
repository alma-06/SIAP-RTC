from pathlib import Path

import pytest

from app.application.e2e_import import EndToEndImportService
from app.application.rtc_import import ImportResult


class FakeService:
    def execute(self, files: list[Path]) -> ImportResult:
        result = ImportResult(files_processed=len(files), rows_read=4)
        return result


def test_e2e_import_requires_files() -> None:
    service = EndToEndImportService(FakeService())
    with pytest.raises(ValueError):
        service.execute([])


def test_e2e_import_returns_report() -> None:
    report = EndToEndImportService(FakeService()).execute([Path("a.xlsx")])
    assert report.files == 1
    assert report.rows_read == 4
