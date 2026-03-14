from __future__ import annotations

from src.modules.auth.domain.entities.tenant import Tenant
from src.modules.auth.infrastructure.models.tenant_model import TenantModel


def to_model(entity: Tenant) -> TenantModel:
    return TenantModel(
        id=entity.id,
        name=entity.name,
        created_at=entity.created_at,
    )


def to_domain(model: TenantModel) -> Tenant:
    return Tenant(
        id=model.id,
        name=model.name,
        created_at=model.created_at,
    )
