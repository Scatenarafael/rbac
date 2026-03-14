from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
AUTHORIZE_ACTION_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/authorize_action_usecase.py"


def test_t4_authorize_action_usecase_file_exists() -> None:
    if not AUTHORIZE_ACTION_USECASE_FILE.exists():
        pytest.fail(
            "Arquivo esperado ainda não implementado: src/modules/auth/application/usecases/authorize_action_usecase.py"
        )


def test_t4_authorize_action_usecase_contract() -> None:
    if not AUTHORIZE_ACTION_USECASE_FILE.exists():
        pytest.fail("AuthorizeActionUseCase ainda não implementado para validar contrato.")

    source = AUTHORIZE_ACTION_USECASE_FILE.read_text()
    assert "class AuthorizeActionUseCase" in source
    assert "async def execute" in source
    assert "permission_code" in source
    assert "tenant_id" in source
    assert "ResolveEffectivePermissionsUseCase" in source
    assert "PermissionCode" in source


def test_t4_authorize_action_usecase_handles_forbidden_scenario() -> None:
    if not AUTHORIZE_ACTION_USECASE_FILE.exists():
        pytest.fail("AuthorizeActionUseCase ainda não implementado para validar cenário de proibição.")

    source = AUTHORIZE_ACTION_USECASE_FILE.read_text()
    assert "ValidationError" in source or "Forbidden" in source
