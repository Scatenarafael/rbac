from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.modules.auth.domain.entities.role import Role
from src.modules.auth.domain.repository_interfaces.role_repository import IRoleRepository
from src.modules.auth.infrastructure.mappers.role_mapper import to_domain, to_model
from src.modules.auth.infrastructure.models.role_model import RoleModel


class RoleRepositorySQLModel(IRoleRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session = session

    async def create(self, data: Role) -> Role:
        model = to_model(data)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return to_domain(model)

    async def get_by_id(self, id: UUID) -> Role | None:
        result = await self.session.execute(select(RoleModel).where(RoleModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_domain(model)

    async def update(self, id: UUID, data: Role) -> Role | None:
        result = await self.session.execute(select(RoleModel).where(RoleModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return None

        model.name = data.name
        model.description = data.description

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return to_domain(model)

    async def delete(self, id: UUID) -> bool:
        result = await self.session.execute(select(RoleModel).where(RoleModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return False

        await self.session.delete(model)
        await self.session.commit()
        return True
