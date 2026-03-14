from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.modules.auth.domain.entities.user import User
from src.modules.auth.domain.exceptions import ValidationError
from src.modules.auth.domain.repository_interfaces.user_repository import IUserRepository


@dataclass(slots=True, frozen=True)
class MeResult:
    user: User


class MeUseCase:
    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    async def execute(self, *, user_id: UUID) -> MeResult:
        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise ValidationError("User not found.")
        return MeResult(user=user)
