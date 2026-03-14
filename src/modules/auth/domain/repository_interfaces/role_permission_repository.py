from __future__ import annotations

from abc import abstractmethod
from uuid import UUID

from src.modules.auth.domain.entities.role_permission import RolePermission
from src.modules.auth.domain.repository_interfaces.repository_base import IRepositoryBase


class IRolePermissionRepository(IRepositoryBase[RolePermission, UUID]):
    @abstractmethod
    async def list_by_role_ids(self, role_ids: list[UUID]) -> list[RolePermission]:
        pass
