from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
ME_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/me_usecase.py"


def test_t3_me_usecase_file_exists() -> None:
    if not ME_USECASE_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/application/usecases/me_usecase.py")


def test_t3_me_usecase_contract() -> None:
    if not ME_USECASE_FILE.exists():
        pytest.fail("MeUseCase ainda não implementado para validar contrato.")

    source = ME_USECASE_FILE.read_text()
    assert "class MeUseCase" in source
    assert "async def execute" in source
    assert "IUserRepository" in source
