from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.application.import_history import ImportHistoryService
from app.infrastructure.orm import Base, ImportBatchModel


def test_import_history_orders_batches_and_validates_limit() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([
            ImportBatchModel(id="b1", started_at=datetime(2026, 8, 1, tzinfo=timezone.utc), imported_count=2, rejected_count=0, duplicate_count=1),
            ImportBatchModel(id="b2", started_at=datetime(2026, 8, 2, tzinfo=timezone.utc), imported_count=3, rejected_count=1, duplicate_count=0),
        ])
        session.commit()
        service = ImportHistoryService(session)
        assert [b.id for b in service.list_batches()] == ["b2", "b1"]
        with pytest.raises(ValueError):
            service.list_batches(0)
