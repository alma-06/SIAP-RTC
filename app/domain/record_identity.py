from __future__ import annotations

import hashlib
import re
import unicodedata
from collections.abc import Mapping

IDENTITY_FIELDS = (
    "pauta_transmision",
    "estado",
    "tiempo_fiscal",
    "canal_base",
    "orden",
    "fecha",
    "dependencia_cam_sen",
    "clave",
    "campana",
    "version",
)


def normalize_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKC", text).strip().upper()
    text = re.sub(r"\s+", " ", text)
    return text


def canonical_value(field: str, value: object) -> str:
    # Field-specific normalization can be expanded as source variants are identified.
    return normalize_text(value)


def canonical_identity(record: Mapping[str, object]) -> str:
    values = [f"{field}={canonical_value(field, record.get(field))}" for field in IDENTITY_FIELDS]
    return "|".join(values)


def record_identity_hash(record: Mapping[str, object]) -> str:
    canonical = canonical_identity(record).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()
