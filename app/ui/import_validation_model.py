from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.ui.preflight_validation import FileValidationResult, PreflightValidator


@dataclass
class ImportValidationModel:
    validator: PreflightValidator

    def validate_files(self, paths: list[Path]) -> list[FileValidationResult]:
        return [self.validator.validate(path) for path in paths]

    @staticmethod
    def can_process(results: list[FileValidationResult]) -> bool:
        return bool(results) and all(result.valid for result in results)
