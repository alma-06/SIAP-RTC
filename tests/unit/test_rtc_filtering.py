"""Contract tests for the CAM. SEN. filtering boundary.

These tests intentionally describe the domain contract independently of Excel I/O.
The processing implementation must preserve only the exact institutional dependency.
"""

from app.domain.rtc_record import RtcRecord


def test_senate_dependency_is_the_institutional_target() -> None:
    record = RtcRecord(
        pauta_transmision="P1", estado="VIGENTE", tiempo_fiscal="F",
        canal_base="C", orden="O1", fecha="2026-08-07",
        dependencia="CAM. SEN.", clave="K", campana="C1", version="V1",
    )
    assert record.dependencia == "CAM. SEN."


def test_non_senate_dependency_is_not_the_target() -> None:
    record = RtcRecord(
        pauta_transmision="P1", estado="VIGENTE", tiempo_fiscal="F",
        canal_base="C", orden="O1", fecha="2026-08-07",
        dependencia="OTRA DEPENDENCIA", clave="K", campana="C1", version="V1",
    )
    assert record.dependencia != "CAM. SEN."
