from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class RefreshSessionModel(SQLModel, table=True):
    __tablename__ = "refresh_sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    tenant_id: UUID | None = Field(default=None, foreign_key="tenants.id", index=True)

    token_jti: str = Field(unique=True, index=True, max_length=128)
    token_hash: str = Field(max_length=1024)

    user_agent: str | None = Field(default=None, max_length=1024)
    ip_address: str | None = Field(default=None, max_length=128)

    is_revoked: bool = Field(default=False)
    replaced_by_token_jti: str | None = Field(default=None, max_length=128)

    expires_at: datetime
    created_at: datetime = Field(default_factory=utcnow)
    revoked_at: datetime | None = Field(default=None)
    last_used_at: datetime | None = Field(default=None)
