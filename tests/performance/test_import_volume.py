"""Opt-in performance benchmark for representative RTC record volumes."""
from __future__ import annotations

import time
from datetime import date

import pytest

from app.domain.rtc_record import RtcRecord


def pytest_addoption(parser):
    parser.addoption("--run-performance", action="store_true", default=False)


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-performance"):
        return
    skip = pytest.mark.skip(reason="performance suite is opt-in")
    for item in items:
        item.add_marker(skip)


@pytest.mark.parametrize("size", [1_000, 10_000, 50_000])
def test_record_construction_volume(size: int) -> None:
    started = time.perf_counter()
    records = [
        RtcRecord(
            pauta_transmision=f"P{i}", estado="VIGENTE", tiempo_fiscal="F",
            canal_base="C", orden=f"O{i}", fecha=date(2026, 8, 7),
            dependencia="CAM. SEN.", clave=f"K{i}", campana="C1", version="V1",
        )
        for i in range(size)
    ]
    elapsed = time.perf_counter() - started
    assert len(records) == size
    assert elapsed < 30
