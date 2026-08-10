from __future__ import annotations

from dataclasses import dataclass

from app.methodology.broadcaster_universe import BroadcasterUniverse
from app.methodology.criterion_78 import Criterion78Result, calculate_criterion_78


@dataclass(frozen=True)
class ConciliationCase:
    case_id: str
    period: str
    source_file: str
    source_hash: str
    universe: BroadcasterUniverse
    impacts: int
    standard_spot_seconds: int = 30
    notes: str | None = None

    def calculate(self) -> Criterion78Result:
        return calculate_criterion_78(
            self.impacts,
            self.universe.as_criterion_78_parameters(self.standard_spot_seconds),
        )

    def evidence_summary(self) -> dict[str, object]:
        result = self.calculate()
        return {
            "case_id": self.case_id,
            "period": self.period,
            "source_file": self.source_file,
            "source_hash": self.source_hash,
            "universe_id": self.universe.universe_id,
            "broadcaster_count": self.universe.total_stations,
            "universe_source": self.universe.source,
            "universe_cutoff_date": self.universe.cutoff_date,
            "universe_methodology": self.universe.methodology,
            "impacts": self.impacts,
            "standard_spot_seconds": self.standard_spot_seconds,
            "total_seconds": result.total_seconds,
            "elapsed_time": result.elapsed_time,
            "interpretation": result.interpretation,
            "notes": self.notes,
        }
