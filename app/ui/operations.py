from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from app.pipeline.integrated import IntegratedPipelineResult, run_integrated_period
from app.validation.rtc_preflight import WorkbookValidation, validate_rtc_workbooks


@dataclass(frozen=True)
class OperationRequest:
    files: tuple[Path, ...]
    period: str
    run_preflight: bool = True


@dataclass(frozen=True)
class OperationResponse:
    preflight: tuple[WorkbookValidation, ...]
    result: IntegratedPipelineResult | None


def execute_operation(request: OperationRequest) -> OperationResponse:
    validations = validate_rtc_workbooks(request.files) if request.run_preflight else ()
    if any(not validation.valid for validation in validations):
        return OperationResponse(validations, None)
    result = run_integrated_period(list(request.files), request.period)
    return OperationResponse(validations, result)
