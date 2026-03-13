from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from ..exceptions import ValidationError
from .base import new_uuid, utcnow


@dataclass(slots=True, kw_only=True)
class User:
    id: UUID = field(default_factory=new_uuid)
    email: str
    password_hash: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = field(default_factory=utcnow)

    def __post_init__(self) -> None:
        self.email = self._normalize_email(self.email)
        self.password_hash = self.password_hash.strip()

        if not self.email:
            raise ValidationError("User email cannot be empty.")

        if not self.password_hash:
            raise ValidationError("User password_hash cannot be empty.")

    @staticmethod
    def _normalize_email(email: str) -> str:
        return email.strip().lower()

    def change_email(self, new_email: str) -> None:
        normalized = self._normalize_email(new_email)
        if not normalized:
            raise ValidationError("User email cannot be empty.")
        self.email = normalized

    def change_password_hash(self, new_password_hash: str) -> None:
        new_password_hash = new_password_hash.strip()
        if not new_password_hash:
            raise ValidationError("User password_hash cannot be empty.")
        self.password_hash = new_password_hash

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def grant_superuser(self) -> None:
        self.is_superuser = True

    def revoke_superuser(self) -> None:
        self.is_superuser = False
