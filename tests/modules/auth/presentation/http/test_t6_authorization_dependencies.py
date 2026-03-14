from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
AUTH_DEPENDENCIES_FILE = PROJECT_ROOT / "src/modules/auth/presentation/http/auth_dependencies.py"


def test_t6_auth_dependencies_file_exists() -> None:
    if not AUTH_DEPENDENCIES_FILE.exists():
        pytest.fail("Arquivo esperado não encontrado: src/modules/auth/presentation/http/auth_dependencies.py")


def test_t6_require_permissions_dependency_contract() -> None:
    source = AUTH_DEPENDENCIES_FILE.read_text()
    assert "def require_permissions" in source, (
        "F6 deve expor dependência `require_permissions` para proteção de endpoints."
    )
    assert "PermissionCode" in source, "require_permissions deve validar permissões com PermissionCode."
    assert "AuthorizeActionUseCase" in source, "require_permissions deve delegar decisão para AuthorizeActionUseCase."


def test_t6_auth_dependencies_expose_current_user_context() -> None:
    source = AUTH_DEPENDENCIES_FILE.read_text()
    assert "get_current_user_context" in source, (
        "F6 deve expor dependência para resolver contexto autenticado do usuário."
    )
    assert "JWTService" in source, "Contexto do usuário deve ser construído a partir de JWT."


def test_t6_auth_dependencies_handle_401_and_403() -> None:
    source = AUTH_DEPENDENCIES_FILE.read_text()
    assert "HTTPException" in source
    assert "401" in source, "F6 deve explicitar resposta 401 para não autenticado."
    assert "403" in source, "F6 deve explicitar resposta 403 para acesso proibido."
