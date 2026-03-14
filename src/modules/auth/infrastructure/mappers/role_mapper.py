from __future__ import annotations

from src.modules.auth.domain.entities.role import Role
from src.modules.auth.infrastructure.models.role_model import RoleModel


def to_model(entity: Role) -> RoleModel:
    return RoleModel(
        id=entity.id,
        name=entity.name,
        description=entity.description,
    )


def to_domain(model: RoleModel) -> Role:
    return Role(
        id=model.id,
        name=model.name,
        description=model.description,
    )
