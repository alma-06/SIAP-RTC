from app.validation.technical_opinion import OpinionInputs, OpinionStatus, determine_opinion


def test_no_real_files_means_not_validated() -> None:
    inputs = OpinionInputs(False, True, True, True, True, True)
    assert determine_opinion(inputs) == OpinionStatus.NO_VALIDADO


def test_critical_failure_rejects_validation() -> None:
    inputs = OpinionInputs(True, False, True, True, True, True)
    assert determine_opinion(inputs) == OpinionStatus.RECHAZADO


def test_missing_documented_limitations_yields_observations() -> None:
    inputs = OpinionInputs(True, True, True, True, True, False)
    assert determine_opinion(inputs) == OpinionStatus.VALIDADO_CON_OBSERVACIONES


def test_complete_validation_is_validated() -> None:
    inputs = OpinionInputs(True, True, True, True, True, True)
    assert determine_opinion(inputs) == OpinionStatus.VALIDADO
