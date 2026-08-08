from app.domain.record_identity import record_identity_hash


def test_identity_ignores_case_and_outer_whitespace() -> None:
    a = {
        "pauta_transmision": "Pauta 01",
        "estado": "ACTIVO",
        "tiempo_fiscal": "00:30",
        "canal_base": "CANAL 1",
        "orden": "10",
        "fecha": "2026-08-01",
        "dependencia_cam_sen": "CAM. SEN.",
        "clave": "ABC",
        "campana": "Campaña X",
        "version": "V1",
    }
    b = {key: (f"  {value.lower()}  " if isinstance(value, str) else value) for key, value in a.items()}
    assert record_identity_hash(a) == record_identity_hash(b)
