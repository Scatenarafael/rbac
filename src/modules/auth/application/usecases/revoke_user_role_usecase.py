from __future__ import annotations

from uuid import UUID

from src.modules.auth.domain.repository_interfaces.user_tenant_role_repository import IUserTenantRoleRepository


class RevokeUserRoleUseCase:
    def __init__(self, user_tenant_role_repository: IUserTenantRoleRepository) -> None:
        self._user_tenant_role_repository = user_tenant_role_repository

    async def execute(
        self,
        *,
        user_id: UUID,
        tenant_id: UUID,
        role_id: UUID,
    ) -> bool:
        return await self._user_tenant_role_repository.delete_by_user_tenant_role(
            user_id=user_id,
            tenant_id=tenant_id,
            role_id=role_id,
        )
