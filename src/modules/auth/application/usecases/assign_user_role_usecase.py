from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.modules.auth.domain.entities.user_tenant_role import UserTenantRole
from src.modules.auth.domain.exceptions import ValidationError
from src.modules.auth.domain.repository_interfaces.user_tenant_role_repository import IUserTenantRoleRepository


@dataclass(slots=True, frozen=True)
class AssignUserRoleResult:
    assignment: UserTenantRole


class AssignUserRoleUseCase:
    def __init__(self, user_tenant_role_repository: IUserTenantRoleRepository) -> None:
        self._user_tenant_role_repository = user_tenant_role_repository

    async def execute(
        self,
        *,
        user_id: UUID,
        tenant_id: UUID,
        role_id: UUID,
    ) -> AssignUserRoleResult:
        existing_assignment = await self._user_tenant_role_repository.get_by_user_tenant_role(
            user_id=user_id,
            tenant_id=tenant_id,
            role_id=role_id,
        )
        if existing_assignment is not None:
            raise ValidationError("User role assignment already exists.")

        assignment = UserTenantRole(
            user_id=user_id,
            tenant_id=tenant_id,
            role_id=role_id,
        )
        created_assignment = await self._user_tenant_role_repository.create(assignment)
        return AssignUserRoleResult(assignment=created_assignment)
