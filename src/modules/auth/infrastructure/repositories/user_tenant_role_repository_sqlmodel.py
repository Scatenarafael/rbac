from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.modules.auth.domain.entities.user_tenant_role import UserTenantRole
from src.modules.auth.domain.repository_interfaces.user_tenant_role_repository import IUserTenantRoleRepository
from src.modules.auth.infrastructure.models.user_tenant_role_model import UserTenantRoleModel


def _to_domain(model: UserTenantRoleModel) -> UserTenantRole:
    return UserTenantRole(
        id=model.id,
        user_id=model.user_id,
        tenant_id=model.tenant_id,
        role_id=model.role_id,
    )


def _to_model(entity: UserTenantRole) -> UserTenantRoleModel:
    return UserTenantRoleModel(
        id=entity.id,
        user_id=entity.user_id,
        tenant_id=entity.tenant_id,
        role_id=entity.role_id,
    )


class UserTenantRoleRepositorySQLModel(IUserTenantRoleRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session = session

    async def create(self, data: UserTenantRole) -> UserTenantRole:
        model = _to_model(data)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return _to_domain(model)

    async def get_by_id(self, id: UUID) -> UserTenantRole | None:
        result = await self.session.execute(select(UserTenantRoleModel).where(UserTenantRoleModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return _to_domain(model)

    async def update(self, id: UUID, data: UserTenantRole) -> UserTenantRole | None:
        result = await self.session.execute(select(UserTenantRoleModel).where(UserTenantRoleModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return None

        model.user_id = data.user_id
        model.tenant_id = data.tenant_id
        model.role_id = data.role_id

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return _to_domain(model)

    async def delete(self, id: UUID) -> bool:
        result = await self.session.execute(select(UserTenantRoleModel).where(UserTenantRoleModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return False

        await self.session.delete(model)
        await self.session.commit()
        return True

    async def get_by_user_tenant_role(
        self,
        *,
        user_id: UUID,
        tenant_id: UUID,
        role_id: UUID,
    ) -> UserTenantRole | None:
        result = await self.session.execute(
            select(UserTenantRoleModel).where(
                UserTenantRoleModel.user_id == user_id,
                UserTenantRoleModel.tenant_id == tenant_id,
                UserTenantRoleModel.role_id == role_id,
            )
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return _to_domain(model)

    async def list_by_user_and_tenant(
        self,
        *,
        user_id: UUID,
        tenant_id: UUID,
    ) -> list[UserTenantRole]:
        result = await self.session.execute(
            select(UserTenantRoleModel).where(
                UserTenantRoleModel.user_id == user_id,
                UserTenantRoleModel.tenant_id == tenant_id,
            )
        )
        models = result.scalars().all()
        return [_to_domain(model) for model in models]

    async def delete_by_user_tenant_role(
        self,
        *,
        user_id: UUID,
        tenant_id: UUID,
        role_id: UUID,
    ) -> bool:
        result = await self.session.execute(
            select(UserTenantRoleModel).where(
                UserTenantRoleModel.user_id == user_id,
                UserTenantRoleModel.tenant_id == tenant_id,
                UserTenantRoleModel.role_id == role_id,
            )
        )
        model = result.scalar_one_or_none()
        if model is None:
            return False

        await self.session.delete(model)
        await self.session.commit()
        return True
