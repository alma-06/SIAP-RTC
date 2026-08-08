from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.application.report_service import RtcReportService
from app.infrastructure.orm import Base


def test_empty_database_cannot_generate_report(tmp_path: Path) -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        with pytest.raises(ValueError, match="no contiene registros"):
            RtcReportService(session).export(tmp_path / "empty.xlsx")
