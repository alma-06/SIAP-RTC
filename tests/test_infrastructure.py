from pathlib import Path

from app.infrastructure.database import initialize_database
from app.shared.config import load_config


def test_load_config(tmp_path: Path) -> None:
    config_file = tmp_path / "application.yml"
    config_file.write_text(
        "app:\n  name: Test SIAP-RTC\n  version: 9.9.9\n", encoding="utf-8"
    )
    config = load_config(config_file)
    assert config.name == "Test SIAP-RTC"
    assert config.version == "9.9.9"


def test_initialize_database(tmp_path: Path) -> None:
    database = tmp_path / "siap_rtc.db"
    initialize_database(database)
    assert database.exists()
