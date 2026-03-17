from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
PROD_VALIDATOR_FILE = PROJECT_ROOT / "src/modules/auth/application/services/auth_production_validator.py"


def test_t8_auth_production_validator_file_exists() -> None:
    if not PROD_VALIDATOR_FILE.exists():
        pytest.fail(
            "Arquivo esperado ainda não implementado: src/modules/auth/application/services/auth_production_validator.py"
        )


def test_t8_auth_production_validator_contract() -> None:
    if not PROD_VALIDATOR_FILE.exists():
        pytest.fail("AuthProductionValidator ainda não implementado para validar contrato.")

    source = PROD_VALIDATOR_FILE.read_text()
    assert "class AuthProductionValidator" in source
    assert "def validate" in source
    assert "Settings" in source
    assert "SECRET_KEY" in source
    assert "COOKIE_SECURE" in source
    assert "COOKIE_SAMESITE" in source
    assert "COOKIE_DOMAIN" in source
    assert "ValidationError" in source or "raise" in source
