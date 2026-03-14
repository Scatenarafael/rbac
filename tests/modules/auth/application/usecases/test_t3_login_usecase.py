from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
LOGIN_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/login_usecase.py"


def test_t3_login_usecase_file_exists() -> None:
    if not LOGIN_USECASE_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/application/usecases/login_usecase.py")


def test_t3_login_usecase_contract() -> None:
    if not LOGIN_USECASE_FILE.exists():
        pytest.fail("LoginUseCase ainda não implementado para validar contrato.")

    source = LOGIN_USECASE_FILE.read_text()
    assert "class LoginUseCase" in source
    assert "async def execute" in source
    assert "PasswordHasher" in source
    assert "JWTService" in source
    assert "RefreshTokenSecurity" in source
    assert "IUserRepository" in source
    assert "IRefreshSessionRepository" in source
