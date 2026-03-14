from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
AUTH_ROUTER_FILE = PROJECT_ROOT / "src/modules/auth/presentation/http/routers/auth_router.py"


def test_t6_auth_router_file_exists() -> None:
    if not AUTH_ROUTER_FILE.exists():
        pytest.fail("Arquivo esperado não encontrado: src/modules/auth/presentation/http/routers/auth_router.py")


def test_t6_auth_router_uses_require_permissions_dependency() -> None:
    source = AUTH_ROUTER_FILE.read_text()
    assert "require_permissions" in source, (
        "F6 deve aplicar dependência `require_permissions` em endpoints protegidos."
    )
    assert "Depends" in source


def test_t6_auth_router_marks_protected_routes() -> None:
    source = AUTH_ROUTER_FILE.read_text()
    protected_hints = [
        "logout-all",
        "me",
        "permissions",
    ]
    if not any(hint in source for hint in protected_hints):
        pytest.fail("Router deve conter rotas protegidas relevantes para autorização.")

    assert "users:read" in source or "auth:me" in source or "auth:logout_all" in source, (
        "F6 deve declarar ao menos um permission code aplicado em rota."
    )
