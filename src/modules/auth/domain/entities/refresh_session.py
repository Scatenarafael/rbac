from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from ..exceptions import ValidationError
from .base import new_uuid, utcnow


@dataclass(slots=True, kw_only=True)
class RefreshSession:
    id: UUID = field(default_factory=new_uuid)
    user_id: UUID
    tenant_id: UUID | None = None

    token_jti: str
    token_hash: str

    user_agent: str | None = None
    ip_address: str | None = None

    is_revoked: bool = False
    replaced_by_token_jti: str | None = None

    expires_at: datetime
    created_at: datetime = field(default_factory=utcnow)
    revoked_at: datetime | None = None
    last_used_at: datetime | None = None

    def __post_init__(self) -> None:
        self.token_jti = self.token_jti.strip()
        self.token_hash = self.token_hash.strip()

        if not self.token_jti:
            raise ValidationError("RefreshSession token_jti cannot be empty.")

        if not self.token_hash:
            raise ValidationError("RefreshSession token_hash cannot be empty.")

        if self.user_agent is not None:
            self.user_agent = self.user_agent.strip() or None

        if self.ip_address is not None:
            self.ip_address = self.ip_address.strip() or None

    def is_expired(self, now: datetime | None = None) -> bool:
        now = now or utcnow()
        return now >= self.expires_at

    def is_active(self, now: datetime | None = None) -> bool:
        return not self.is_revoked and not self.is_expired(now)

    def mark_as_used(self, when: datetime | None = None) -> None:
        self.last_used_at = when or utcnow()

    def revoke(
        self,
        *,
        replaced_by_token_jti: str | None = None,
        when: datetime | None = None,
    ) -> None:
        self.is_revoked = True
        self.revoked_at = when or utcnow()
        self.replaced_by_token_jti = replaced_by_token_jti

    def rotate(
        self,
        *,
        new_token_jti: str,
        new_token_hash: str,
        new_expires_at: datetime,
        when: datetime | None = None,
    ) -> "RefreshSession":
        self.revoke(
            replaced_by_token_jti=new_token_jti,
            when=when,
        )

        return RefreshSession(
            user_id=self.user_id,
            tenant_id=self.tenant_id,
            token_jti=new_token_jti.strip(),
            token_hash=new_token_hash.strip(),
            user_agent=self.user_agent,
            ip_address=self.ip_address,
            expires_at=new_expires_at,
        )
