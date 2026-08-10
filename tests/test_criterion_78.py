import pytest

from app.methodology.criterion_78 import Criterion78Parameters, calculate_criterion_78


def test_criterion_78_calculates_parameterized_time() -> None:
    result = calculate_criterion_78(
        10,
        Criterion78Parameters(
            broadcaster_count=1377,
            standard_spot_seconds=30,
            parameter_source="CRT fixture",
            cutoff_date="2026-06-30",
        ),
    )
    assert result.total_seconds == 413100
    assert result.elapsed_time == "114:45:00"
    assert "no constituye" in result.interpretation


def test_parameters_reject_invalid_broadcaster_count() -> None:
    with pytest.raises(ValueError):
        Criterion78Parameters(broadcaster_count=0)


def test_negative_impacts_are_rejected() -> None:
    with pytest.raises(ValueError):
        calculate_criterion_78(-1, Criterion78Parameters(broadcaster_count=1377))
