from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from src.modules.auth.application.services.jwt_service import JWTService
from src.modules.auth.application.services.refresh_token_security import RefreshTokenSecurity
from src.modules.auth.domain.exceptions import ValidationError
from src.modules.auth.domain.repository_interfaces.refresh_session import IRefreshSessionRepository


@dataclass(slots=True, frozen=True)
class RefreshSessionResult:
    access_token: str
    refresh_token: str


def _exp_claim_to_datetime(exp_claim: object) -> datetime:
    if isinstance(exp_claim, datetime):
        return exp_claim
    if isinstance(exp_claim, (int, float)):
        return datetime.fromtimestamp(exp_claim, tz=UTC)
    raise ValidationError("Token exp claim is invalid.")


class RefreshSessionUseCase:
    def __init__(
        self,
        *,
        refresh_session_repository: IRefreshSessionRepository,
        jwt_service: JWTService,
        refresh_token_security: RefreshTokenSecurity,
    ) -> None:
        self._refresh_session_repository = refresh_session_repository
        self._jwt_service = jwt_service
        self._refresh_token_security = refresh_token_security

    async def execute(self, *, refresh_token: str) -> RefreshSessionResult:
        # Logical transaction boundary for refresh token rotation.
        payload = self._jwt_service.decode_token(refresh_token, expected_type="refresh")

        session_jti = str(payload.get("jti", "")).strip()
        if not session_jti:
            raise ValidationError("Refresh token jti is missing.")

        session = await self._refresh_session_repository.get_by_jti(session_jti)
        if session is None:
            raise ValidationError("Refresh session not found.")

        # Reuse detection: if this token already rotated once, it was reused.
        # The replaced_by_token_jti marker is our idempotency and theft signal.
        replaced_by_token_jti = session.replaced_by_token_jti
        if replaced_by_token_jti is not None:
            await self._revoke_all_user_sessions(session.user_id)
            raise ValidationError("Refresh token reuse detected.")

        if not session.is_active():
            raise ValidationError("Refresh session is not active.")

        if not self._refresh_token_security.verify_refresh_token(refresh_token, session.token_hash):
            raise ValidationError("Refresh token does not match stored session.")

        user_id_raw = str(payload.get("sub", "")).strip()
        if not user_id_raw:
            raise ValidationError("Refresh token subject is missing.")

        try:
            user_uuid = UUID(user_id_raw)
        except ValueError as exc:
            raise ValidationError("Refresh token subject is invalid.") from exc

        tenant_id = payload.get("tenant_id")
        tenant_id_str = str(tenant_id) if tenant_id is not None else None

        new_refresh_token = self._jwt_service.create_refresh_token(
            subject=str(user_uuid),
            tenant_id=tenant_id_str,
        )
        new_refresh_payload = self._jwt_service.decode_token(new_refresh_token, expected_type="refresh")
        new_jti = str(new_refresh_payload.get("jti", "")).strip()
        if not new_jti:
            raise ValidationError("New refresh token jti is missing.")

        rotated_session = session.rotate(
            new_token_jti=new_jti,
            new_token_hash=self._refresh_token_security.hash_refresh_token(new_refresh_token),
            new_expires_at=_exp_claim_to_datetime(new_refresh_payload.get("exp")),
        )

        await self._refresh_session_repository.update(session.id, session)
        await self._refresh_session_repository.create(rotated_session)

        new_access_token = self._jwt_service.create_access_token(
            subject=str(user_uuid),
            tenant_id=tenant_id_str,
        )

        return RefreshSessionResult(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )

    async def _revoke_all_user_sessions(self, user_id: UUID) -> None:
        sessions = await self._refresh_session_repository.list_by_user_id(user_id)
        for existing_session in sessions:
            if existing_session.is_revoked:
                continue
            existing_session.revoke()
            await self._refresh_session_repository.update(existing_session.id, existing_session)
