from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Criterion78Inputs:
    impacts: int
    broadcasters: int
    seconds_per_impact: int = 30


@dataclass(frozen=True)
class Criterion78Result:
    inputs: Criterion78Inputs
    total_seconds: int

    @property
    def days(self) -> int:
        return self.total_seconds // 86400

    @property
    def remainder_seconds(self) -> int:
        return self.total_seconds % 86400

    @property
    def hms(self) -> tuple[int, int, int]:
        seconds = self.remainder_seconds
        return seconds // 3600, (seconds % 3600) // 60, seconds % 60


def calculate_criterion78(inputs: Criterion78Inputs) -> Criterion78Result:
    if inputs.impacts < 0 or inputs.broadcasters < 0 or inputs.seconds_per_impact < 0:
        raise ValueError("Los parámetros del Criterio 78 no pueden ser negativos")
    total_seconds = inputs.impacts * inputs.broadcasters * inputs.seconds_per_impact
    return Criterion78Result(inputs, total_seconds)
