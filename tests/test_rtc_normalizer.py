from app.application.rtc_normalizer import homologate_headers, normalize_dependency, normalize_header


def test_normalize_header_removes_accents_and_spacing() -> None:
    assert normalize_header("  Campaña  ") == "campana"
    assert normalize_header("Pauta de transmisión") == "pauta de transmision"


def test_homologate_headers() -> None:
    result = homologate_headers(["Pauta de transmisión", "Campaña", "Dependencia CAM. SEN."])
    assert result["Pauta de transmisión"] == "pauta_transmision"
    assert result["Campaña"] == "campana"
    assert result["Dependencia CAM. SEN."] == "dependencia"


def test_normalize_dependency() -> None:
    assert normalize_dependency("CAM SEN") == "CAM. SEN."
    assert normalize_dependency("Cam. Sen.") == "CAM. SEN."
