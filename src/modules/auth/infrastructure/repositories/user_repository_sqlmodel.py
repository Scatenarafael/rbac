from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.modules.auth.domain.entities.user import User
from src.modules.auth.domain.repository_interfaces.user_repository import IUserRepository
from src.modules.auth.domain.value_objects.emails import Email
from src.modules.auth.infrastructure.mappers.user_mapper import to_domain, to_model
from src.modules.auth.infrastructure.models.user_model import UserModel


class UserRepositorySQLModel(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session = session

    async def create(self, data: User) -> User:
        model = to_model(data)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return to_domain(model)

    async def get_by_id(self, id: UUID) -> User | None:
        result = await self.session.execute(select(UserModel).where(UserModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_domain(model)

    async def update(self, id: UUID, data: User) -> User | None:
        result = await self.session.execute(select(UserModel).where(UserModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return None

        model.email = data.email
        model.password_hash = data.password_hash
        model.is_active = data.is_active
        model.is_superuser = data.is_superuser
        model.created_at = data.created_at

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return to_domain(model)

    async def delete(self, id: UUID) -> bool:
        result = await self.session.execute(select(UserModel).where(UserModel.id == id))
        model = result.scalar_one_or_none()
        if model is None:
            return False

        await self.session.delete(model)
        await self.session.commit()
        return True

    async def get_by_email(self, email: Email) -> User | None:
        result = await self.session.execute(select(UserModel).where(UserModel.email == email.value))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_domain(model)
