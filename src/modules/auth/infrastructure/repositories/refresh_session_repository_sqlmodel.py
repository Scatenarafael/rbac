from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.modules.auth.domain.entities.refresh_session import RefreshSession
from src.modules.auth.domain.repository_interfaces.refresh_session import IRefreshSessionRepository
from src.modules.auth.infrastructure.mappers.refresh_session_mapper import to_domain, to_model
from src.modules.auth.infrastructure.models.refresh_session_model import RefreshSessionModel


class RefreshSessionRepositorySQLModel(IRefreshSessionRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session = session

    async def create(self, data: RefreshSession) -> RefreshSession:
        model = to_model(data)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return to_domain(model)

    async def get_by_id(self, id: UUID) -> RefreshSession | None:
        result = await self.session.execute(select(RefreshSessionModel).where(RefreshSessionModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_domain(model)

    async def update(self, id: UUID, data: RefreshSession) -> RefreshSession | None:
        result = await self.session.execute(select(RefreshSessionModel).where(RefreshSessionModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return None

        model.user_id = data.user_id
        model.tenant_id = data.tenant_id
        model.token_jti = data.token_jti
        model.token_hash = data.token_hash
        model.user_agent = data.user_agent
        model.ip_address = data.ip_address
        model.is_revoked = data.is_revoked
        model.replaced_by_token_jti = data.replaced_by_token_jti
        model.expires_at = data.expires_at
        model.created_at = data.created_at
        model.revoked_at = data.revoked_at
        model.last_used_at = data.last_used_at

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return to_domain(model)

    async def delete(self, id: UUID) -> bool:
        result = await self.session.execute(select(RefreshSessionModel).where(RefreshSessionModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return False

        await self.session.delete(model)
        await self.session.commit()
        return True

    async def get_by_jti(self, jti: str) -> RefreshSession | None:
        result = await self.session.execute(
            select(RefreshSessionModel).where(RefreshSessionModel.token_jti == jti.strip())
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_domain(model)
