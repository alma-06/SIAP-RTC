from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from app.export.package_manifest import _hash_file


@dataclass(frozen=True)
class HistoricalPeriod:
    period: str
    evidence_id: str
    package_path: str
    package_sha256: str


class HistoricalStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.index_path = self.root / "HistoricalIndex.json"

    def periods(self) -> tuple[HistoricalPeriod, ...]:
        if not self.index_path.exists():
            return ()
        data = json.loads(self.index_path.read_text(encoding="utf-8"))
        return tuple(HistoricalPeriod(**item) for item in data.get("periods", []))

    def register_period(self, period: str, evidence_id: str, package_path: str | Path) -> HistoricalPeriod:
        package = Path(package_path)
        if not package.exists():
            raise FileNotFoundError(package)
        existing = {item.period: item for item in self.periods()}
        if period in existing:
            raise ValueError(f"El periodo {period} ya está registrado")
        relative = str(package)
        record = HistoricalPeriod(period, evidence_id, relative, _hash_file(package))
        periods = [*self.periods(), record]
        periods.sort(key=lambda item: item.period)
        self.index_path.write_text(
            json.dumps({"periods": [item.__dict__ for item in periods]}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return record

    def verify(self) -> tuple[bool, list[str]]:
        errors: list[str] = []
        for item in self.periods():
            path = Path(item.package_path)
            if not path.exists():
                errors.append(f"Falta paquete histórico: {item.period}")
                continue
            if _hash_file(path) != item.package_sha256:
                errors.append(f"SHA-256 histórico inconsistente: {item.period}")
        return not errors, errors
