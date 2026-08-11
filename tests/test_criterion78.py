from app.reconciliation.criterion78 import Criterion78Inputs, calculate_criterion78


def test_criterion78_calculates_total_seconds_and_hms() -> None:
    result = calculate_criterion78(Criterion78Inputs(10, 1377, 30))
    assert result.total_seconds == 413100
    assert result.days == 4
    assert result.hms == (18, 45, 0)


def test_criterion78_rejects_negative_parameters() -> None:
    try:
        calculate_criterion78(Criterion78Inputs(-1, 10, 30))
    except ValueError:
        pass
    else:
        raise AssertionError("Se esperaba ValueError")
