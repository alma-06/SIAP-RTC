"""Opt-in end-to-end persistence benchmark for SIAP-RTC."""
from __future__ import annotations

import time
from pathlib import Path

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.infrastructure.orm import Base, RtcRecordModel


def pytest_addoption(parser):
    parser.addoption("--run-performance", action="store_true", default=False)


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-performance"):
        return
    skip = pytest.mark.skip(reason="performance suite is opt-in")
    for item in items:
        item.add_marker(skip)


@pytest.mark.parametrize("size", [1_000, 10_000, 50_000])
def test_sqlite_insert_and_count_volume(tmp_path: Path, size: int) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / f'perf_{size}.db'}")
    Base.metadata.create_all(engine)
    started = time.perf_counter()
    with Session(engine) as session:
        session.add_all([
            RtcRecordModel(
                id=f"r-{i}", batch_id="performance", pauta_transmision=f"P{i}",
                estado="VIGENTE", tiempo_fiscal="F", canal_base="C", orden=f"O{i}",
                fecha=None, dependencia="CAM. SEN.", clave=f"K{i}", campana="C1", version="V1",
            ) for i in range(size)
        ])
        session.commit()
        count = session.scalar(select(func.count(RtcRecordModel.id)))
    elapsed = time.perf_counter() - started
    assert count == size
    assert elapsed < 60
