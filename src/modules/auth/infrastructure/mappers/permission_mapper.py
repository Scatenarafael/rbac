from __future__ import annotations

from src.modules.auth.domain.entities.permission import Permission
from src.modules.auth.infrastructure.models.permission_model import PermissionModel


def to_model(entity: Permission) -> PermissionModel:
    return PermissionModel(
        id=entity.id,
        name=entity.name,
        description=entity.description,
    )


def to_domain(model: PermissionModel) -> Permission:
    return Permission(
        id=model.id,
        name=model.name,
        description=model.description,
    )
