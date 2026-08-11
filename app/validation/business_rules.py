from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re
from typing import Mapping

REQUIRED_COLUMNS = (
    "Pauta de transmisión", "Estado", "Tiempo Fiscal", "Canal Base", "Orden",
    "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión",
)

SENATE_ALIASES = frozenset({
    "cam. sen.", "cam sen", "camara de senadores", "cámara de senadores",
})


@dataclass(frozen=True)
class RuleDecision:
    valid: bool
    senate: bool
    warnings: tuple[str, ...]


def normalize_text(value: object) -> str:
    return re.sub(r"\s+", " ", "" if value is None else str(value).strip()).casefold()


def is_senate_dependency(value: object) -> bool:
    return normalize_text(value) in SENATE_ALIASES


def classify_record(record: Mapping[str, object]) -> RuleDecision:
    warnings: list[str] = []
    missing = [column for column in REQUIRED_COLUMNS if column not in record]
    if missing:
        return RuleDecision(False, False, (f"Faltan columnas: {', '.join(missing)}",))

    senate = is_senate_dependency(record.get("Dependencia CAM. SEN."))
    if not senate:
        warnings.append("Registro fuera del universo de Cámara de Senadores")

    if not str(record.get("Clave") or "").strip():
        warnings.append("Clave vacía")
    if not str(record.get("Orden") or "").strip():
        warnings.append("Orden vacío")
    if not str(record.get("Fecha") or "").strip():
        warnings.append("Fecha vacía")

    valid = senate and not any(w.startswith("Clave vacía") or w.startswith("Orden vacío") or w.startswith("Fecha vacía") for w in warnings)
    return RuleDecision(valid, senate, tuple(warnings))


def canonical_duplicate_key(record: Mapping[str, object]) -> tuple[str, ...]:
    fields = ("Fecha", "Orden", "Clave", "Versión", "Canal Base", "Dependencia CAM. SEN.")
    return tuple(normalize_text(record.get(field)) for field in fields)
