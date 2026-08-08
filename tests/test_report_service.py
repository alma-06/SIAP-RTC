from pathlib import Path

import pytest

from app.application.report_service import RtcReportService


class FakeQuery:
    def list_records(self, **filters):
        return []


def test_report_service_rejects_empty_query(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr("app.application.report_service.RtcQueryService", lambda session: FakeQuery())
    with pytest.raises(ValueError, match="no contiene registros"):
        RtcReportService(object()).export(tmp_path / "r.xlsx")
