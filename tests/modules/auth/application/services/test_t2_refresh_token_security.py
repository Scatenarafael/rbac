from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
REFRESH_SECURITY_FILE = PROJECT_ROOT / "src/modules/auth/application/services/refresh_token_security.py"


def test_t2_refresh_token_security_file_exists() -> None:
    if not REFRESH_SECURITY_FILE.exists():
        pytest.fail(
            "Arquivo esperado ainda não implementado: src/modules/auth/application/services/refresh_token_security.py"
        )


def test_t2_refresh_token_security_contract() -> None:
    if not REFRESH_SECURITY_FILE.exists():
        pytest.fail("RefreshTokenSecurity ainda não implementado para validar contrato.")

    source = REFRESH_SECURITY_FILE.read_text()
    assert "class RefreshTokenSecurity" in source
    assert "def hash_refresh_token" in source
    assert "def verify_refresh_token" in source
    assert "def generate_token_jti" in source


def test_t2_refresh_token_security_jti_generation_has_unique_strategy() -> None:
    if not REFRESH_SECURITY_FILE.exists():
        pytest.fail("RefreshTokenSecurity ainda não implementado para validar estratégia de jti.")

    source = REFRESH_SECURITY_FILE.read_text()
    assert "uuid4" in source or "secrets" in source, (
        "RefreshTokenSecurity deve gerar jti com estratégia de unicidade."
    )
