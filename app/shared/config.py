"""Configuration loading for SIAP-RTC."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Immutable application configuration."""

    name: str = "SIAP-RTC"
    version: str = "0.1.0a1"
    data_dir: Path = Path("data")
    log_dir: Path = Path("logs")


def load_config(path: Path) -> AppConfig:
    """Load application settings from a YAML file.

    Missing optional keys fall back to safe project defaults.
    """
    raw: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    app = raw.get("app", {})
    return AppConfig(
        name=str(app.get("name", "SIAP-RTC")),
        version=str(app.get("version", "0.1.0a1")),
        data_dir=Path(str(app.get("data_dir", "data"))),
        log_dir=Path(str(app.get("log_dir", "logs"))),
    )
