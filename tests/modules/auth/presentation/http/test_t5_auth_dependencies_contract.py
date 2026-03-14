from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
AUTH_DEPENDENCIES_FILE = PROJECT_ROOT / "src/modules/auth/presentation/http/auth_dependencies.py"


def test_t5_auth_dependencies_file_exists() -> None:
    if not AUTH_DEPENDENCIES_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/presentation/http/auth_dependencies.py")


def test_t5_auth_dependencies_contract() -> None:
    if not AUTH_DEPENDENCIES_FILE.exists():
        pytest.fail("Dependências de auth ainda não implementadas para validar contrato.")

    source = AUTH_DEPENDENCIES_FILE.read_text()
    assert "Depends" in source
    assert "get_session" in source
    assert "get_register_usecase" in source
    assert "get_login_usecase" in source
    assert "get_refresh_session_usecase" in source
    assert "get_logout_usecase" in source
    assert "get_me_usecase" in source
