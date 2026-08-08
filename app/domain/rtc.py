"""Canonical RTC record used by all import sources."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.domain.value_objects import RtcRecordKey


@dataclass(frozen=True, slots=True)
class RtcRecord:
    """Canonical representation of one RTC transmission spot."""

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
    source_row_number: int | None = None

    @property
    def business_key(self) -> RtcRecordKey:
        return RtcRecordKey(
            self.pauta_transmision, self.estado, self.tiempo_fiscal, self.canal_base,
            self.orden, self.fecha, self.dependencia, self.clave, self.campana, self.version,
        )

    @property
    def is_senate_record(self) -> bool:
        normalized = " ".join(self.dependencia.upper().replace(".", " ").split())
        return normalized in {"CAM SEN", "CAMARA SENADORES", "CAMARA DE SENADORES"}
