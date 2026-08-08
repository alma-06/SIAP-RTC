"""Normalization services for heterogeneous RTC Excel publications."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping


CANONICAL_HEADERS: dict[str, str] = {
    "pauta de transmision": "pauta_transmision",
    "pauta transmisión": "pauta_transmision",
    "pauta": "pauta_transmision",
    "estado": "estado",
    "tiempo fiscal": "tiempo_fiscal",
    "canal base": "canal_base",
    "orden": "orden",
    "fecha": "fecha",
    "dependencia cam sen": "dependencia",
    "dependencia cam. sen.": "dependencia",
    "dependencia": "dependencia",
    "clave": "clave",
    "campaña": "campana",
    "campana": "campana",
    "versión": "version",
    "version": "version",
}


def normalize_header(value: object) -> str:
    """Normalize a spreadsheet header for matching."""
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().replace("_", " ")
    text = re.sub(r"[^a-z0-9. ]+", " ", text)
    return " ".join(text.split())


def homologate_headers(headers: list[object]) -> dict[object, str]:
    """Map source headers to canonical field names when recognized."""
    aliases = {normalize_header(k): v for k, v in CANONICAL_HEADERS.items()}
    return {header: aliases[normalize_header(header)] for header in headers if normalize_header(header) in aliases}


def normalize_dependency(value: object) -> str:
    """Canonicalize the Senate dependency designation."""
    text = "" if value is None else str(value).upper()
    text = " ".join(text.replace(".", " ").split())
    if text in {"CAM SEN", "CAMARA SENADORES", "CAMARA DE SENADORES"}:
        return "CAM. SEN."
    return " ".join(text.split())
