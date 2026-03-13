from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from .base import new_uuid


@dataclass(slots=True, kw_only=True)
class UserTenantRole:
    id: UUID = field(default_factory=new_uuid)
    user_id: UUID
    tenant_id: UUID
    role_id: UUID

    def change_role(self, new_role_id: UUID) -> None:
        self.role_id = new_role_id

    def move_to_tenant(self, new_tenant_id: UUID) -> None:
        self.tenant_id = new_tenant_id
