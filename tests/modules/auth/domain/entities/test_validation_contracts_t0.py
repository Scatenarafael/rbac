from datetime import timedelta
from uuid import uuid4

import pytest

from src.modules.auth.domain.entities.permission import Permission
from src.modules.auth.domain.entities.refresh_session import RefreshSession
from src.modules.auth.domain.entities.role import Role
from src.modules.auth.domain.entities.role_permission import RolePermission
from src.modules.auth.domain.entities.tenant import Tenant
from src.modules.auth.domain.entities.user import User
from src.modules.auth.domain.entities.base import utcnow
from src.modules.auth.domain.exceptions import ValidationError


def test_user_empty_email_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        User(email=" ", password_hash="hash")


def test_tenant_empty_name_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        Tenant(name=" ")


def test_role_empty_name_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        Role(name=" ")


def test_permission_empty_name_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        Permission(name=" ")


def test_refresh_session_empty_jti_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        RefreshSession(
            user_id=uuid4(),
            token_jti=" ",
            token_hash="token-hash",
            expires_at=utcnow() + timedelta(days=1),
        )


def test_refresh_session_empty_token_hash_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        RefreshSession(
            user_id=uuid4(),
            token_jti="jti",
            token_hash=" ",
            expires_at=utcnow() + timedelta(days=1),
        )


def test_role_permission_equal_ids_raises_validation_error() -> None:
    same_id = uuid4()
    with pytest.raises(ValidationError):
        RolePermission(role_id=same_id, permission_id=same_id)
