from __future__ import annotations

from src.modules.auth.domain.entities.refresh_session import RefreshSession
from src.modules.auth.infrastructure.models.refresh_session_model import RefreshSessionModel


def to_model(entity: RefreshSession) -> RefreshSessionModel:
    return RefreshSessionModel(
        id=entity.id,
        user_id=entity.user_id,
        tenant_id=entity.tenant_id,
        token_jti=entity.token_jti,
        token_hash=entity.token_hash,
        user_agent=entity.user_agent,
        ip_address=entity.ip_address,
        is_revoked=entity.is_revoked,
        replaced_by_token_jti=entity.replaced_by_token_jti,
        expires_at=entity.expires_at,
        created_at=entity.created_at,
        revoked_at=entity.revoked_at,
        last_used_at=entity.last_used_at,
    )


def to_domain(model: RefreshSessionModel) -> RefreshSession:
    return RefreshSession(
        id=model.id,
        user_id=model.user_id,
        tenant_id=model.tenant_id,
        token_jti=model.token_jti,
        token_hash=model.token_hash,
        user_agent=model.user_agent,
        ip_address=model.ip_address,
        is_revoked=model.is_revoked,
        replaced_by_token_jti=model.replaced_by_token_jti,
        expires_at=model.expires_at,
        created_at=model.created_at,
        revoked_at=model.revoked_at,
        last_used_at=model.last_used_at,
    )
