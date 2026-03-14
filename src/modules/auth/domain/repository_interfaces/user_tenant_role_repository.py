from __future__ import annotations

from abc import abstractmethod
from uuid import UUID

from src.modules.auth.domain.entities.user_tenant_role import UserTenantRole
from src.modules.auth.domain.repository_interfaces.repository_base import IRepositoryBase


class IUserTenantRoleRepository(IRepositoryBase[UserTenantRole, UUID]):
    @abstractmethod
    async def get_by_user_tenant_role(
        self,
        *,
        user_id: UUID,
        tenant_id: UUID,
        role_id: UUID,
    ) -> UserTenantRole | None:
        pass

    @abstractmethod
    async def list_by_user_and_tenant(
        self,
        *,
        user_id: UUID,
        tenant_id: UUID,
    ) -> list[UserTenantRole]:
        pass

    @abstractmethod
    async def delete_by_user_tenant_role(
        self,
        *,
        user_id: UUID,
        tenant_id: UUID,
        role_id: UUID,
    ) -> bool:
        pass
