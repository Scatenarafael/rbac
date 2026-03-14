from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.modules.auth.domain.entities.tenant import Tenant
from src.modules.auth.domain.repository_interfaces.tenant_repository import ITenantRepository
from src.modules.auth.infrastructure.mappers.tenant_mapper import to_domain, to_model
from src.modules.auth.infrastructure.models.tenant_model import TenantModel


class TenantRepositorySQLModel(ITenantRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session = session

    async def create(self, data: Tenant) -> Tenant:
        model = to_model(data)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return to_domain(model)

    async def get_by_id(self, id: UUID) -> Tenant | None:
        result = await self.session.execute(select(TenantModel).where(TenantModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_domain(model)

    async def update(self, id: UUID, data: Tenant) -> Tenant | None:
        result = await self.session.execute(select(TenantModel).where(TenantModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return None

        model.name = data.name
        model.created_at = data.created_at

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return to_domain(model)

    async def delete(self, id: UUID) -> bool:
        result = await self.session.execute(select(TenantModel).where(TenantModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return False

        await self.session.delete(model)
        await self.session.commit()
        return True
