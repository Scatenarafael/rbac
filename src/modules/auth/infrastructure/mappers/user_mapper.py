from __future__ import annotations

from src.modules.auth.domain.entities.user import User
from src.modules.auth.infrastructure.models.user_model import UserModel


def to_model(entity: User) -> UserModel:
    return UserModel(
        id=entity.id,
        email=entity.email,
        password_hash=entity.password_hash,
        is_active=entity.is_active,
        is_superuser=entity.is_superuser,
        created_at=entity.created_at,
    )


def to_domain(model: UserModel) -> User:
    return User(
        id=model.id,
        email=model.email,
        password_hash=model.password_hash,
        is_active=model.is_active,
        is_superuser=model.is_superuser,
        created_at=model.created_at,
    )
