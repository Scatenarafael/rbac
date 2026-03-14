from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.modules.auth.domain.entities.role_permission import RolePermission
from src.modules.auth.domain.repository_interfaces.role_permission_repository import IRolePermissionRepository
from src.modules.auth.infrastructure.models.role_permission_model import RolePermissionModel


def _to_domain(model: RolePermissionModel) -> RolePermission:
    return RolePermission(
        role_id=model.role_id,
        permission_id=model.permission_id,
    )


def _to_model(entity: RolePermission) -> RolePermissionModel:
    return RolePermissionModel(
        role_id=entity.role_id,
        permission_id=entity.permission_id,
    )


class RolePermissionRepositorySQLModel(IRolePermissionRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session = session

    async def create(self, data: RolePermission) -> RolePermission:
        model = _to_model(data)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return _to_domain(model)

    async def get_by_id(self, id: UUID) -> RolePermission | None:
        result = await self.session.execute(select(RolePermissionModel).where(RolePermissionModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return _to_domain(model)

    async def update(self, id: UUID, data: RolePermission) -> RolePermission | None:
        result = await self.session.execute(select(RolePermissionModel).where(RolePermissionModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return None

        model.role_id = data.role_id
        model.permission_id = data.permission_id

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return _to_domain(model)

    async def delete(self, id: UUID) -> bool:
        result = await self.session.execute(select(RolePermissionModel).where(RolePermissionModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return False

        await self.session.delete(model)
        await self.session.commit()
        return True

    async def list_by_role_ids(self, role_ids: list[UUID]) -> list[RolePermission]:
        if not role_ids:
            return []

        result = await self.session.execute(
            select(RolePermissionModel).where(RolePermissionModel.role_id.in_(role_ids))
        )
        models = result.scalars().all()
        return [_to_domain(model) for model in models]
