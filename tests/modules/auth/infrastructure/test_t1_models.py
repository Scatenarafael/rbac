from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]


def require_file(relative_path: str) -> Path:
    file_path = PROJECT_ROOT / relative_path
    if not file_path.exists():
        pytest.fail(f"Arquivo esperado ainda não implementado: {relative_path}")
    return file_path

REQUIRED_MODEL_FILES = [
    "src/modules/auth/infrastructure/models/user_model.py",
    "src/modules/auth/infrastructure/models/tenant_model.py",
    "src/modules/auth/infrastructure/models/role_model.py",
    "src/modules/auth/infrastructure/models/permission_model.py",
    "src/modules/auth/infrastructure/models/role_permission_model.py",
    "src/modules/auth/infrastructure/models/user_tenant_role_model.py",
    "src/modules/auth/infrastructure/models/refresh_session_model.py",
]


def test_t1_required_sqlmodel_files_exist() -> None:
    for relative_path in REQUIRED_MODEL_FILES:
        require_file(relative_path)


def test_t1_user_model_defines_unique_email_constraint() -> None:
    source = require_file("src/modules/auth/infrastructure/models/user_model.py").read_text()
    assert "email" in source
    assert "unique=True" in source or "UniqueConstraint" in source, (
        "UserModel deve garantir unicidade de email."
    )


def test_t1_refresh_session_model_defines_unique_jti_constraint() -> None:
    source = require_file("src/modules/auth/infrastructure/models/refresh_session_model.py").read_text()
    assert "token_jti" in source
    assert "unique=True" in source or "UniqueConstraint" in source, (
        "RefreshSessionModel deve garantir unicidade de token_jti."
    )


def test_t1_rbac_relation_models_define_composite_uniques() -> None:
    role_permission_source = require_file(
        "src/modules/auth/infrastructure/models/role_permission_model.py"
    ).read_text()
    user_tenant_role_source = require_file(
        "src/modules/auth/infrastructure/models/user_tenant_role_model.py"
    ).read_text()

    assert "UniqueConstraint" in role_permission_source, (
        "RolePermissionModel deve definir unique composto (role_id, permission_id)."
    )
    assert "UniqueConstraint" in user_tenant_role_source, (
        "UserTenantRoleModel deve definir unique composto ao menos para (user_id, tenant_id, role_id)."
    )
