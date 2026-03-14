from __future__ import annotations

from dataclasses import dataclass

from src.modules.auth.application.services.password_hasher import PasswordHasher
from src.modules.auth.domain.entities.user import User
from src.modules.auth.domain.exceptions import ValidationError
from src.modules.auth.domain.repository_interfaces.user_repository import IUserRepository
from src.modules.auth.domain.value_objects.emails import Email


@dataclass(slots=True, frozen=True)
class RegisterResult:
    user: User


class RegisterUseCase:
    def __init__(self, user_repository: IUserRepository, password_hasher: PasswordHasher) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def execute(self, *, email: str, password: str) -> RegisterResult:
        email_vo = Email(email)
        existing_user = await self._user_repository.get_by_email(email_vo)
        if existing_user is not None:
            raise ValidationError("User with this email already exists.")

        password_hash = self._password_hasher.hash_password(password)
        user = User(email=email_vo.value, password_hash=password_hash)
        created_user = await self._user_repository.create(user)
        return RegisterResult(user=created_user)
