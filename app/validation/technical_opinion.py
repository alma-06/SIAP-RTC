from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OpinionStatus(str, Enum):
    NO_VALIDADO = "NO_VALIDADO"
    VALIDADO_CON_OBSERVACIONES = "VALIDADO_CON_OBSERVACIONES"
    VALIDADO = "VALIDADO"
    RECHAZADO = "RECHAZADO"


@dataclass(frozen=True)
class OpinionInputs:
    real_files_reviewed: bool
    critical_tests_passed: bool
    blocking_findings_closed: bool
    reconciliation_complete: bool
    criterion78_reproducible: bool
    limitations_documented: bool


def determine_opinion(inputs: OpinionInputs) -> OpinionStatus:
    if not inputs.real_files_reviewed:
        return OpinionStatus.NO_VALIDADO
    critical_ok = (
        inputs.critical_tests_passed
        and inputs.blocking_findings_closed
        and inputs.reconciliation_complete
        and inputs.criterion78_reproducible
    )
    if not critical_ok:
        return OpinionStatus.RECHAZADO
    if not inputs.limitations_documented:
        return OpinionStatus.VALIDADO_CON_OBSERVACIONES
    return OpinionStatus.VALIDADO
