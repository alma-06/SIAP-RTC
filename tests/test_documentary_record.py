import pytest

from app.validation.documentary_record import DocumentaryRecord, DocumentaryRegister


def test_documentary_record_requires_file_and_hash(tmp_path) -> None:
    register = DocumentaryRegister(tmp_path / "documents.json")
    record = DocumentaryRecord("EV-001", "OFICIO", "Documento", "OF-001", "2026-08-11", "Senado", "docs/oficio.pdf", "abc")
    assert register.add(record) == record
    with pytest.raises(ValueError):
        register.add(record)


def test_documentary_record_rejects_missing_integrity_data(tmp_path) -> None:
    register = DocumentaryRegister(tmp_path / "documents.json")
    record = DocumentaryRecord("EV-002", "PDF", "Documento", "", "2026-08-11", "RTC", "docs/a.pdf", "")
    with pytest.raises(ValueError):
        register.add(record)
