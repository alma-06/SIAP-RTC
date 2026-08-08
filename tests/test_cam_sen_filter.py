from app.processing.cam_sen_filter import CamSenFilter, normalize_dependency
from app.processing.rtc_reader import NormalizedRTCRecord


def record(dependency: str) -> NormalizedRTCRecord:
    return NormalizedRTCRecord(
        values={"dependencia_cam_sen": dependency},
        source_row=2,
        source_sheet="Pauta",
    )


def test_dependency_normalization() -> None:
    assert normalize_dependency("  Cám. Sen.  ") == "CAM SEN"


def test_cam_sen_is_accepted() -> None:
    decision = CamSenFilter().apply(record("CAM. SEN."))
    assert decision.accepted is True
    assert decision.reason == "CAM_SEN_ACCEPTED"


def test_other_dependency_is_rejected() -> None:
    decision = CamSenFilter().apply(record("CAMARA DE DIPUTADOS"))
    assert decision.accepted is False
    assert decision.reason == "DEPENDENCIA_NO_CAM_SEN"
