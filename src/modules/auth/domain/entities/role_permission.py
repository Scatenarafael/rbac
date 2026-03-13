from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ..exceptions import ValidationError


@dataclass(slots=True, kw_only=True, frozen=True)
class RolePermission:
    role_id: UUID
    permission_id: UUID

    def __post_init__(self) -> None:
        if self.role_id == self.permission_id:
            raise ValidationError("RolePermission role_id and permission_id must be different.")
