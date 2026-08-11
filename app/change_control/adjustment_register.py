from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class Adjustment:
    adjustment_id: str
    finding_code: str
    classification: str
    justification: str
    evidence: tuple[str, ...]
    test_reference: str
    status: str = "PROPOSED"


class AdjustmentRegister:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def list(self) -> tuple[Adjustment, ...]:
        if not self.path.exists():
            return ()
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return tuple(Adjustment(**item) for item in data.get("adjustments", []))

    def propose(self, adjustment: Adjustment) -> Adjustment:
        items = list(self.list())
        if any(item.adjustment_id == adjustment.adjustment_id for item in items):
            raise ValueError(f"Ajuste duplicado: {adjustment.adjustment_id}")
        if not adjustment.evidence:
            raise ValueError("Un ajuste debe tener evidencia")
        if not adjustment.test_reference:
            raise ValueError("Un ajuste debe tener una prueba asociada")
        items.append(adjustment)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({"adjustments": [item.__dict__ for item in items]}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return adjustment
