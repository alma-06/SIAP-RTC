"""Immutable value objects used by the SIAP-RTC domain."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class FileHash:
    """SHA-256 fingerprint of an imported source file."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if len(normalized) != 64 or any(c not in "0123456789abcdef" for c in normalized):
            raise ValueError("FileHash must contain exactly 64 hexadecimal characters")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class RtcRecordKey:
    """Stable business key used as a first-class duplicate-detection value."""

    pauta_transmision: str
    estado: str
    tiempo_fiscal: str
    canal_base: str
    orden: str
    fecha: date
    dependencia: str
    clave: str
    campana: str
    version: str

    def normalized(self) -> tuple[str, ...]:
        """Return a normalized tuple suitable for deterministic comparison."""
        return (
            self.pauta_transmision.strip().upper(),
            self.estado.strip().upper(),
            self.tiempo_fiscal.strip().upper(),
            self.canal_base.strip().upper(),
            self.orden.strip().upper(),
            self.fecha.isoformat(),
            self.dependencia.strip().upper(),
            self.clave.strip().upper(),
            self.campana.strip().upper(),
            self.version.strip().upper(),
        )
