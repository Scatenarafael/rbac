from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
REVOKE_ROLE_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/revoke_user_role_usecase.py"


def test_t4_revoke_user_role_usecase_file_exists() -> None:
    if not REVOKE_ROLE_USECASE_FILE.exists():
        pytest.fail(
            "Arquivo esperado ainda não implementado: src/modules/auth/application/usecases/revoke_user_role_usecase.py"
        )


def test_t4_revoke_user_role_usecase_contract() -> None:
    if not REVOKE_ROLE_USECASE_FILE.exists():
        pytest.fail("RevokeUserRoleUseCase ainda não implementado para validar contrato.")

    source = REVOKE_ROLE_USECASE_FILE.read_text()
    assert "class RevokeUserRoleUseCase" in source
    assert "async def execute" in source
    assert "user_id" in source
    assert "tenant_id" in source
    assert "role_id" in source
    assert "IUserTenantRoleRepository" in source
