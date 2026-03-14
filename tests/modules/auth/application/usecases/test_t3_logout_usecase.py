from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
LOGOUT_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/logout_usecase.py"


def test_t3_logout_usecase_file_exists() -> None:
    if not LOGOUT_USECASE_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/application/usecases/logout_usecase.py")


def test_t3_logout_usecase_contract() -> None:
    if not LOGOUT_USECASE_FILE.exists():
        pytest.fail("LogoutUseCase ainda não implementado para validar contrato.")

    source = LOGOUT_USECASE_FILE.read_text()
    assert "class LogoutUseCase" in source
    assert "async def execute" in source
    assert "IRefreshSessionRepository" in source
    assert "revoke" in source
