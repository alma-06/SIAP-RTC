"""Contract tests for RTC duplicate identity.

The canonical key is intentionally tested at the domain boundary so future
changes to Excel parsing cannot silently alter duplicate semantics.
"""

from app.domain.rtc_record import RtcRecord


def test_equivalent_records_have_equal_identity_fields() -> None:
    kwargs = dict(
        pauta_transmision="P1", estado="VIGENTE", tiempo_fiscal="F",
        canal_base="C", orden="O1", fecha="2026-08-07",
        dependencia="CAM. SEN.", clave="K", campana="C1", version="V1",
    )
    first = RtcRecord(**kwargs)
    second = RtcRecord(**kwargs)
    assert first == second
