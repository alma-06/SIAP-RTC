from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class ReleaseCheck:
    name: str
    passed: bool
    blocking: bool
    detail: str = ""


@dataclass(frozen=True)
class ReleaseCandidateReport:
    version: str
    checks: tuple[ReleaseCheck, ...]

    @property
    def ready(self) -> bool:
        return all(check.passed for check in self.checks if check.blocking)


def build_release_candidate_report(
    version: str,
    checks: Sequence[ReleaseCheck],
) -> ReleaseCandidateReport:
    return ReleaseCandidateReport(version, tuple(checks))
