from datetime import datetime
from uuid import uuid4

from app.application.import_batches import ImportBatchService
from app.domain.entities import ImportBatch
from app.domain.repositories import ImportBatchRepository


class InMemoryBatchRepository(ImportBatchRepository):
    def __init__(self) -> None:
        self.items: dict[str, ImportBatch] = {}

    def add(self, batch: ImportBatch) -> None:
        self.items[str(batch.id)] = batch

    def get(self, batch_id):
        return self.items.get(str(batch_id))


def test_import_batch_service_lifecycle() -> None:
    repository = InMemoryBatchRepository()
    service = ImportBatchService(repository)
    batch = service.start([uuid4()], datetime(2026, 8, 1, 10, 0))
    service.finish(batch, datetime(2026, 8, 1, 10, 5))
    assert repository.get(batch.id) is batch
    assert batch.finished_at is not None
