from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
REGISTER_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/register_usecase.py"


def test_t3_register_usecase_file_exists() -> None:
    if not REGISTER_USECASE_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/application/usecases/register_usecase.py")


def test_t3_register_usecase_contract() -> None:
    if not REGISTER_USECASE_FILE.exists():
        pytest.fail("RegisterUseCase ainda não implementado para validar contrato.")

    source = REGISTER_USECASE_FILE.read_text()
    assert "class RegisterUseCase" in source
    assert "async def execute" in source
    assert "PasswordHasher" in source
    assert "IUserRepository" in source
