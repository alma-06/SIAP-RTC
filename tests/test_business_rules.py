from app.validation.business_rules import canonical_duplicate_key, classify_record

HEADERS = ["Pauta de transmisión", "Estado", "Tiempo Fiscal", "Canal Base", "Orden", "Fecha", "Dependencia CAM. SEN.", "Clave", "Campaña", "Versión"]


def record(**overrides):
    value = {key: "x" for key in HEADERS}
    value.update({"Dependencia CAM. SEN.": "CAM. SEN.", "Orden": "O1", "Fecha": "11/08/2026", "Clave": "C1"})
    value.update(overrides)
    return value


def test_classify_valid_senate_record() -> None:
    decision = classify_record(record())
    assert decision.valid
    assert decision.senate
    assert decision.warnings == ()


def test_classify_non_senate_record() -> None:
    decision = classify_record(record(**{"Dependencia CAM. SEN.": "Otra dependencia"}))
    assert not decision.valid
    assert not decision.senate


def test_duplicate_key_is_stable() -> None:
    first = canonical_duplicate_key(record())
    second = canonical_duplicate_key(record(**{"Campaña": "different"}))
    assert first == second
