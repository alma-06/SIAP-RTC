import pytest

from app.change_control.adjustment_register import Adjustment, AdjustmentRegister


def test_adjustment_requires_evidence_and_test(tmp_path) -> None:
    register = AdjustmentRegister(tmp_path / "adjustments.json")
    with pytest.raises(ValueError):
        register.propose(Adjustment("ADJ-001", "COUNT-001", "TECHNICAL", "Cambio justificado", (), "T-001"))
    with pytest.raises(ValueError):
        register.propose(Adjustment("ADJ-002", "COUNT-001", "TECHNICAL", "Cambio justificado", ("EV-1",), ""))


def test_adjustment_is_registered_once(tmp_path) -> None:
    register = AdjustmentRegister(tmp_path / "adjustments.json")
    adjustment = Adjustment("ADJ-001", "COUNT-001", "TECHNICAL", "Cambio justificado", ("EV-1",), "T-001")
    register.propose(adjustment)
    assert register.list() == (adjustment,)
    with pytest.raises(ValueError):
        register.propose(adjustment)
