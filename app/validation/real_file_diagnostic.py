from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib


@dataclass(frozen=True)
class DiagnosticFinding:
    severity: str
    code: str
    message: str


@dataclass(frozen=True)
class RealFileDiagnostic:
    filename: str
    sha256: str
    size_bytes: int
    findings: tuple[DiagnosticFinding, ...]

    @property
    def blocking(self) -> bool:
        return any(item.severity == "BLOQUEANTE" for item in self.findings)


def diagnose_file(path: str | Path) -> RealFileDiagnostic:
    source = Path(path)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    findings: list[DiagnosticFinding] = []
    if source.suffix.casefold() not in {".xlsx", ".xlsm"}:
        findings.append(DiagnosticFinding("BLOQUEANTE", "EXTENSION", "Extensión no compatible con el diagnóstico RTC"))
    return RealFileDiagnostic(source.name, digest, source.stat().st_size, tuple(findings))
