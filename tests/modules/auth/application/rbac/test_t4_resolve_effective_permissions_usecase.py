from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
RESOLVE_PERMISSIONS_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/resolve_effective_permissions_usecase.py"


def test_t4_resolve_effective_permissions_usecase_file_exists() -> None:
    if not RESOLVE_PERMISSIONS_USECASE_FILE.exists():
        pytest.fail(
            "Arquivo esperado ainda não implementado: "
            "src/modules/auth/application/usecases/resolve_effective_permissions_usecase.py"
        )


def test_t4_resolve_effective_permissions_usecase_contract() -> None:
    if not RESOLVE_PERMISSIONS_USECASE_FILE.exists():
        pytest.fail("ResolveEffectivePermissionsUseCase ainda não implementado para validar contrato.")

    source = RESOLVE_PERMISSIONS_USECASE_FILE.read_text()
    assert "class ResolveEffectivePermissionsUseCase" in source
    assert "async def execute" in source
    assert "user_id" in source
    assert "tenant_id" in source
    assert "IRolePermissionRepository" in source
    assert "IUserTenantRoleRepository" in source


def test_t4_resolve_effective_permissions_usecase_mentions_superuser_bypass() -> None:
    if not RESOLVE_PERMISSIONS_USECASE_FILE.exists():
        pytest.fail("ResolveEffectivePermissionsUseCase ainda não implementado para validar regra de superuser.")

    source = RESOLVE_PERMISSIONS_USECASE_FILE.read_text().lower()
    assert "superuser" in source or "is_superuser" in source
