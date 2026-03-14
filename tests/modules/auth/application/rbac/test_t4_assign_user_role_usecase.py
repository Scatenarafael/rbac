from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
ASSIGN_ROLE_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/assign_user_role_usecase.py"


def test_t4_assign_user_role_usecase_file_exists() -> None:
    if not ASSIGN_ROLE_USECASE_FILE.exists():
        pytest.fail(
            "Arquivo esperado ainda não implementado: src/modules/auth/application/usecases/assign_user_role_usecase.py"
        )


def test_t4_assign_user_role_usecase_contract() -> None:
    if not ASSIGN_ROLE_USECASE_FILE.exists():
        pytest.fail("AssignUserRoleUseCase ainda não implementado para validar contrato.")

    source = ASSIGN_ROLE_USECASE_FILE.read_text()
    assert "class AssignUserRoleUseCase" in source
    assert "async def execute" in source
    assert "user_id" in source
    assert "tenant_id" in source
    assert "role_id" in source
    assert "IUserTenantRoleRepository" in source
