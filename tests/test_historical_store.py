from app.history.historical_store import HistoricalStore


def test_historical_store_registers_period_once_and_verifies(tmp_path) -> None:
    package = tmp_path / "SIAP-RTC_2026-Q2.zip"
    package.write_bytes(b"package-q2")
    store = HistoricalStore(tmp_path / "history")

    record = store.register_period("2026-Q2", "EV-2026-Q2", package)
    assert record.period == "2026-Q2"
    assert len(store.periods()) == 1
    valid, errors = store.verify()
    assert valid
    assert errors == []

    try:
        store.register_period("2026-Q2", "EV-OTHER", package)
    except ValueError:
        pass
    else:
        raise AssertionError("El periodo duplicado debió rechazarse")
