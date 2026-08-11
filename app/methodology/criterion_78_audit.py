from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any

from app.methodology.criterion_78 import Criterion78Parameters, Criterion78Result, calculate_criterion_78


@dataclass(frozen=True)
class Criterion78AuditRecord:
    criterion: str
    period: str
    impacts: int
    broadcaster_count: int
    standard_spot_seconds: int
    parameter_source: str | None
    cutoff_date: str | None
    total_seconds: int
    elapsed_time: str
    result_type: str
    interpretation: str
    input_fingerprint: str


def _fingerprint(period: str, impacts: int, parameters: Criterion78Parameters) -> str:
    payload = {
        "period": period,
        "impacts": impacts,
        "broadcaster_count": parameters.broadcaster_count,
        "standard_spot_seconds": parameters.standard_spot_seconds,
        "impacts_per_day": parameters.impacts_per_day,
        "parameter_source": parameters.parameter_source,
        "cutoff_date": parameters.cutoff_date,
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(canonical.encode("utf-8")).hexdigest()


def calculate_criterion_78_audited(
    period: str, impacts: int, parameters: Criterion78Parameters
) -> tuple[Criterion78Result, Criterion78AuditRecord]:
    result = calculate_criterion_78(impacts, parameters)
    audit = Criterion78AuditRecord(
        criterion="Criterio 78",
        period=period,
        impacts=result.impacts,
        broadcaster_count=result.broadcaster_count,
        standard_spot_seconds=result.spot_seconds,
        parameter_source=parameters.parameter_source,
        cutoff_date=parameters.cutoff_date,
        total_seconds=result.total_seconds,
        elapsed_time=result.elapsed_time,
        result_type="calculado",
        interpretation=result.interpretation,
        input_fingerprint=_fingerprint(period, impacts, parameters),
    )
    return result, audit


def audit_record_to_dict(record: Criterion78AuditRecord) -> dict[str, Any]:
    return asdict(record)
