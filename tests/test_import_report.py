from pathlib import Path

from app.application.import_report import ImportReport
from app.application.rtc_import import ImportIssue, ImportResult


def test_import_report_projects_result() -> None:
    source = Path("rtc.xlsx")
    result = ImportResult(files_processed=1, rows_read=12, duplicates=2, rejected=1)
    result.issues.append(ImportIssue(source, "Pauta", 9, "Fecha inválida"))
    result.file_hashes[source] = "a" * 64
    report = ImportReport.from_result(result)
    assert report.files == 1
    assert report.rows_read == 12
    assert report.accepted == 0
    assert report.duplicates == 2
    assert report.rejected == 1
    assert "Fecha inválida" in report.issues[0]
