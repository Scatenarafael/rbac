from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]


def require_file(relative_path: str) -> Path:
    file_path = PROJECT_ROOT / relative_path
    if not file_path.exists():
        pytest.fail(f"Arquivo esperado ainda não implementado: {relative_path}")
    return file_path

REQUIRED_REPOSITORY_FILES = [
    "src/modules/auth/infrastructure/repositories/user_repository_sqlmodel.py",
    "src/modules/auth/infrastructure/repositories/tenant_repository_sqlmodel.py",
    "src/modules/auth/infrastructure/repositories/role_repository_sqlmodel.py",
    "src/modules/auth/infrastructure/repositories/permission_repository_sqlmodel.py",
    "src/modules/auth/infrastructure/repositories/refresh_session_repository_sqlmodel.py",
]

BASE_METHODS = ["create", "get_by_id", "update", "delete"]


def test_t1_required_repository_files_exist() -> None:
    for relative_path in REQUIRED_REPOSITORY_FILES:
        require_file(relative_path)


def test_t1_repositories_implement_base_async_methods() -> None:
    for relative_path in REQUIRED_REPOSITORY_FILES:
        source = require_file(relative_path).read_text()
        for method_name in BASE_METHODS:
            assert f"async def {method_name}" in source, (
                f"{relative_path} deve implementar método assíncrono `{method_name}`."
            )


def test_t1_user_repository_implements_get_by_email() -> None:
    source = require_file(
        "src/modules/auth/infrastructure/repositories/user_repository_sqlmodel.py"
    ).read_text()
    assert "async def get_by_email" in source


def test_t1_refresh_session_repository_implements_get_by_jti() -> None:
    source = require_file(
        "src/modules/auth/infrastructure/repositories/refresh_session_repository_sqlmodel.py"
    ).read_text()
    assert "async def get_by_jti" in source
