from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BroadcasterUniverse:
    """Auditable universe of broadcasters used by a calculation."""

    universe_id: str
    total_stations: int
    source: str
    cutoff_date: str
    methodology: str
    source_file: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.universe_id.strip():
            raise ValueError("El universo debe tener identificador")
        if self.total_stations <= 0:
            raise ValueError("El total de estaciones debe ser mayor que cero")
        if not self.source.strip():
            raise ValueError("La fuente es obligatoria")
        if not self.cutoff_date.strip():
            raise ValueError("La fecha de corte es obligatoria")
        if not self.methodology.strip():
            raise ValueError("La metodología de conteo es obligatoria")

    def as_criterion_78_parameters(self, standard_spot_seconds: int = 30):
        from app.methodology.criterion_78 import Criterion78Parameters
        return Criterion78Parameters(
            broadcaster_count=self.total_stations,
            standard_spot_seconds=standard_spot_seconds,
            parameter_source=self.source,
            cutoff_date=self.cutoff_date,
        )
