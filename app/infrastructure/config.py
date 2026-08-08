from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class AppPaths:
    root: Path
    data: Path
    imports: Path
    reports: Path
    logs: Path
    backups: Path

    @classmethod
    def from_environment(cls) -> "AppPaths":
        configured = os.getenv("SIAP_RTC_DATA_DIR")
        root = Path(configured).expanduser() if configured else Path(os.getenv("APPDATA", Path.home())) / "SIAP-RTC"
        return cls(
            root=root,
            data=root / "data",
            imports=root / "imports",
            reports=root / "reports",
            logs=root / "logs",
            backups=root / "backups",
        )

    def ensure(self) -> "AppPaths":
        for path in (self.root, self.data, self.imports, self.reports, self.logs, self.backups):
            path.mkdir(parents=True, exist_ok=True)
        return self

    @property
    def database(self) -> Path:
        return self.data / "siap_rtc.db"
