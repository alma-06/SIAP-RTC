import pytest
from datetime import timedelta

from app.domain.duration import duration_to_seconds, seconds_to_excel_elapsed, seconds_to_hhmmss


def test_mmss_to_seconds() -> None:
    assert duration_to_seconds("00:30") == 30


def test_hhmmss_to_seconds() -> None:
    assert duration_to_seconds("01:02:03") == 3723


def test_excel_fraction_to_seconds() -> None:
    assert duration_to_seconds(30 / 86400) == 30


def test_timedelta_to_seconds() -> None:
    assert duration_to_seconds(timedelta(seconds=45)) == 45


def test_elapsed_format_preserves_hours_over_24() -> None:
    assert seconds_to_excel_elapsed(90061) == "25:01:01"


def test_hhmmss_format() -> None:
    assert seconds_to_hhmmss(3723) == "01:02:03"


@pytest.mark.parametrize("value", ["01:60", "00:00:60", "-00:30", "abc"])
def test_invalid_duration_is_rejected(value: str) -> None:
    with pytest.raises(ValueError):
        duration_to_seconds(value)
