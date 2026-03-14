from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
LOGOUT_ALL_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/logout_all_usecase.py"


def test_t3_logout_all_usecase_file_exists() -> None:
    if not LOGOUT_ALL_USECASE_FILE.exists():
        pytest.fail(
            "Arquivo esperado ainda não implementado: src/modules/auth/application/usecases/logout_all_usecase.py"
        )


def test_t3_logout_all_usecase_contract() -> None:
    if not LOGOUT_ALL_USECASE_FILE.exists():
        pytest.fail("LogoutAllUseCase ainda não implementado para validar contrato.")

    source = LOGOUT_ALL_USECASE_FILE.read_text()
    assert "class LogoutAllUseCase" in source
    assert "async def execute" in source
    assert "IRefreshSessionRepository" in source
    assert "revoke" in source
