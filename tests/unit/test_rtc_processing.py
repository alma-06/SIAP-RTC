from pathlib import Path

from app.application.rtc_import import ImportIssue, ImportResult


def test_import_result_tracks_files_rows_and_issues() -> None:
    result = ImportResult(files_processed=2, rows_read=100, duplicates=7, rejected=3)
    result.issues.append(ImportIssue(Path("semana.xlsx"), "Pauta", 12, "Encabezado no reconocido"))
    assert result.files_processed == 2
    assert result.rows_read == 100
    assert result.duplicates == 7
    assert result.rejected == 3
    assert result.issues[0].row == 12


def test_import_result_starts_with_empty_acceptance_set() -> None:
    result = ImportResult()
    assert result.accepted == []
    assert result.file_hashes == {}
