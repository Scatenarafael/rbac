from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
AUTH_SCHEMAS_FILE = PROJECT_ROOT / "src/modules/auth/presentation/http/schemas/auth_schemas.py"


def test_t5_auth_schemas_file_exists() -> None:
    if not AUTH_SCHEMAS_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/presentation/http/schemas/auth_schemas.py")


def test_t5_auth_schemas_contract() -> None:
    if not AUTH_SCHEMAS_FILE.exists():
        pytest.fail("Auth schemas ainda não implementados para validar contrato.")

    source = AUTH_SCHEMAS_FILE.read_text()
    assert "BaseModel" in source
    assert "class RegisterRequest" in source
    assert "class LoginRequest" in source
    assert "class LoginResponse" in source
    assert "class RefreshResponse" in source
    assert "class MeResponse" in source
