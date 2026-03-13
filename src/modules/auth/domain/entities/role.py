from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ..exceptions import ValidationError
from .base import new_uuid


@dataclass(slots=True, kw_only=True)
class Role:
    id: UUID = field(default_factory=new_uuid)
    name: str
    description: str | None = None

    def __post_init__(self) -> None:
        self.name = self.name.strip().lower()
        if not self.name:
            raise ValidationError("Role name cannot be empty.")

        if self.description is not None:
            self.description = self.description.strip() or None

    def rename(self, new_name: str) -> None:
        new_name = new_name.strip().lower()
        if not new_name:
            raise ValidationError("Role name cannot be empty.")
        self.name = new_name

    def change_description(self, description: str | None) -> None:
        if description is None:
            self.description = None
            return
        self.description = description.strip() or None
