from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.modules.auth.domain.exceptions import ValidationError
from src.modules.auth.domain.repository_interfaces.permission_repository import IPermissionRepository
from src.modules.auth.domain.repository_interfaces.role_permission_repository import IRolePermissionRepository
from src.modules.auth.domain.repository_interfaces.user_repository import IUserRepository
from src.modules.auth.domain.repository_interfaces.user_tenant_role_repository import IUserTenantRoleRepository


@dataclass(slots=True, frozen=True)
class ResolveEffectivePermissionsResult:
    permissions: set[str]
    is_superuser: bool


class ResolveEffectivePermissionsUseCase:
    def __init__(
        self,
        *,
        user_repository: IUserRepository,
        user_tenant_role_repository: IUserTenantRoleRepository,
        role_permission_repository: IRolePermissionRepository,
        permission_repository: IPermissionRepository,
    ) -> None:
        self._user_repository = user_repository
        self._user_tenant_role_repository = user_tenant_role_repository
        self._role_permission_repository = role_permission_repository
        self._permission_repository = permission_repository

    async def execute(
        self,
        *,
        user_id: UUID,
        tenant_id: UUID,
    ) -> ResolveEffectivePermissionsResult:
        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise ValidationError("User not found.")

        if user.is_superuser:
            return ResolveEffectivePermissionsResult(permissions={"*"}, is_superuser=True)

        assignments = await self._user_tenant_role_repository.list_by_user_and_tenant(
            user_id=user_id,
            tenant_id=tenant_id,
        )
        if not assignments:
            return ResolveEffectivePermissionsResult(permissions=set(), is_superuser=False)

        role_ids = sorted({assignment.role_id for assignment in assignments}, key=str)
        role_permissions = await self._role_permission_repository.list_by_role_ids(role_ids)

        permission_ids = sorted({item.permission_id for item in role_permissions}, key=str)
        effective_permissions: set[str] = set()

        for permission_id in permission_ids:
            permission = await self._permission_repository.get_by_id(permission_id)
            if permission is None:
                continue
            effective_permissions.add(permission.name)

        return ResolveEffectivePermissionsResult(
            permissions=effective_permissions,
            is_superuser=False,
        )
