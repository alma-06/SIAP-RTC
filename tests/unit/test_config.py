from pathlib import Path

from app.infrastructure.config import AppPaths


def test_paths_are_separated_from_application_root(tmp_path: Path) -> None:
    paths = AppPaths(root=tmp_path, data=tmp_path / "data", imports=tmp_path / "imports", reports=tmp_path / "reports", logs=tmp_path / "logs", backups=tmp_path / "backups")
    paths.ensure()
    assert paths.database == tmp_path / "data" / "siap_rtc.db"
    assert all(p.exists() for p in [paths.data, paths.imports, paths.reports, paths.logs, paths.backups])
