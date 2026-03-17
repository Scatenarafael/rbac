from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
AUTH_SEED_FILE = PROJECT_ROOT / "src/modules/auth/application/services/auth_seed_service.py"


def test_t8_auth_seed_service_file_exists() -> None:
    if not AUTH_SEED_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/application/services/auth_seed_service.py")


def test_t8_auth_seed_service_contract() -> None:
    if not AUTH_SEED_FILE.exists():
        pytest.fail("AuthSeedService ainda não implementado para validar contrato.")

    source = AUTH_SEED_FILE.read_text()
    assert "class AuthSeedService" in source
    assert "async def seed_defaults" in source
    assert "IPermissionRepository" in source
    assert "IRoleRepository" in source
    assert "IRolePermissionRepository" in source
    assert "IUserRepository" in source
    assert "idempot" in source.lower(), (
        "F8 deve explicitar comportamento idempotente no seed de roles/permissões/admin."
    )
