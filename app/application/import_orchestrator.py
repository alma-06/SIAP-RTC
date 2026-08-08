from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.infrastructure.import_transaction import ImportTransaction
from app.processing.cam_sen_filter import CamSenFilter
from app.processing.rtc_reader import RTCExcelReader
from app.ui.import_result import FileImportResult, ImportBatchResult
from app.ui.preflight_validation import PreflightValidator


@dataclass
class ImportOrchestrator:
    database_path: Path
    validator: PreflightValidator
    reader: RTCExcelReader
    cam_sen_filter: CamSenFilter

    def process(self, paths: list[Path], batch_id: str) -> ImportBatchResult:
        batch = ImportBatchResult(batch_id=batch_id)
        validation = [self.validator.validate(path) for path in paths]
        if any(not item.valid for item in validation):
            batch.status = "ERROR"
            batch.files = [
                FileImportResult(
                    filename=item.path.name,
                    sha256=item.sha256,
                    status="INVÁLIDO" if not item.valid else "VÁLIDO",
                    error=item.error,
                )
                for item in validation
            ]
            return batch

        transaction = ImportTransaction(self.database_path)
        try:
            with transaction.begin(batch_id) as connection:
                for item in validation:
                    result = self._process_file(
                        connection, item.path, item.sha256, batch_id
                    )
                    batch.files.append(result)
            batch.finish(True)
        except Exception as exc:
            batch.status = "ERROR"
            if not batch.files:
                batch.files.append(
                    FileImportResult(
                        filename="LOTE", sha256="", status="ERROR", error=str(exc)
                    )
                )
        return batch

    def _process_file(
        self, connection, path: Path, sha256: str, batch_id: str
    ) -> FileImportResult:
        normalized = self.reader.read(path)
        accepted, decisions = self.cam_sen_filter.filter(normalized)
        new_records = 0
        duplicates = 0

        for record in accepted:
            if ImportTransaction.insert_record_or_audit_duplicate(
                connection,
                record.values,
                batch_id=batch_id,
                source_filename=path.name,
            ):
                new_records += 1
            else:
                duplicates += 1

        return FileImportResult(
            filename=path.name,
            sha256=sha256,
            status="PROCESADO",
            records_read=len(normalized),
            cam_sen_records=len(accepted),
            duplicates=duplicates,
            rejected=len(normalized) - len(accepted),
            new_records=new_records,
        )
