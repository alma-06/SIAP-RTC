from __future__ import annotations

from dataclasses import dataclass

from app.domain.duration import seconds_to_excel_elapsed


@dataclass(frozen=True)
class Criterion78Parameters:
    broadcaster_count: int
    standard_spot_seconds: int = 30
    impacts_per_day: int | None = None
    parameter_source: str | None = None
    cutoff_date: str | None = None

    def __post_init__(self) -> None:
        if self.broadcaster_count <= 0:
            raise ValueError("El número de radiodifusoras debe ser mayor que cero")
        if self.standard_spot_seconds <= 0:
            raise ValueError("La duración estándar debe ser mayor que cero")
        if self.impacts_per_day is not None and self.impacts_per_day < 0:
            raise ValueError("Los impactos diarios no pueden ser negativos")


@dataclass(frozen=True)
class Criterion78Result:
    impacts: int
    broadcaster_count: int
    spot_seconds: int
    total_seconds: int
    elapsed_time: str
    interpretation: str


def calculate_criterion_78(impacts: int, parameters: Criterion78Parameters) -> Criterion78Result:
    if impacts < 0:
        raise ValueError("Los impactos no pueden ser negativos")

    total_seconds = impacts * parameters.broadcaster_count * parameters.standard_spot_seconds
    return Criterion78Result(
        impacts=impacts,
        broadcaster_count=parameters.broadcaster_count,
        spot_seconds=parameters.standard_spot_seconds,
        total_seconds=total_seconds,
        elapsed_time=seconds_to_excel_elapsed(total_seconds),
        interpretation=(
            "Tiempo calculado conforme a la metodología parametrizada; "
            "no constituye por sí mismo evidencia de transmisión efectiva."
        ),
    )
