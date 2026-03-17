from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from src.modules.auth.application.services.auth_metrics_service import AuthMetricsService
from src.modules.auth.application.services.jwt_service import JWTService
from src.modules.auth.application.services.password_hasher import PasswordHasher
from src.modules.auth.application.services.refresh_token_security import RefreshTokenSecurity
from src.modules.auth.domain.entities.refresh_session import RefreshSession
from src.modules.auth.domain.exceptions import ValidationError
from src.modules.auth.domain.repository_interfaces.refresh_session import IRefreshSessionRepository
from src.modules.auth.domain.repository_interfaces.user_repository import IUserRepository
from src.modules.auth.domain.value_objects.emails import Email


@dataclass(slots=True, frozen=True)
class LoginResult:
    access_token: str
    refresh_token: str


def _exp_claim_to_datetime(exp_claim: object) -> datetime:
    if isinstance(exp_claim, datetime):
        return exp_claim
    if isinstance(exp_claim, (int, float)):
        return datetime.fromtimestamp(exp_claim, tz=UTC)
    raise ValidationError("Token exp claim is invalid.")


class LoginUseCase:
    def __init__(
        self,
        *,
        user_repository: IUserRepository,
        refresh_session_repository: IRefreshSessionRepository,
        password_hasher: PasswordHasher,
        jwt_service: JWTService,
        refresh_token_security: RefreshTokenSecurity,
        auth_metrics_service: AuthMetricsService | None = None,
    ) -> None:
        self._user_repository = user_repository
        self._refresh_session_repository = refresh_session_repository
        self._password_hasher = password_hasher
        self._jwt_service = jwt_service
        self._refresh_token_security = refresh_token_security
        self._auth_metrics_service = auth_metrics_service or AuthMetricsService()

    async def execute(
        self,
        *,
        email: str,
        password: str,
        tenant_id: str | None = None,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> LoginResult:
        try:
            email_vo = Email(email)
            user = await self._user_repository.get_by_email(email_vo)
            if user is None:
                raise ValidationError("Invalid credentials.")

            if not user.is_active:
                raise ValidationError("Inactive user.")

            if not self._password_hasher.verify_password(password, user.password_hash):
                raise ValidationError("Invalid credentials.")

            access_token = self._jwt_service.create_access_token(
                subject=str(user.id),
                tenant_id=tenant_id,
            )
            refresh_token = self._jwt_service.create_refresh_token(
                subject=str(user.id),
                tenant_id=tenant_id,
            )

            refresh_payload = self._jwt_service.decode_token(refresh_token, expected_type="refresh")
            refresh_jti = str(refresh_payload.get("jti", "")).strip()
            if not refresh_jti:
                raise ValidationError("Refresh token jti is missing.")

            refresh_session = RefreshSession(
                user_id=user.id,
                token_jti=refresh_jti,
                token_hash=self._refresh_token_security.hash_refresh_token(refresh_token),
                user_agent=user_agent,
                ip_address=ip_address,
                expires_at=_exp_claim_to_datetime(refresh_payload.get("exp")),
            )
            await self._refresh_session_repository.create(refresh_session)
        except ValidationError:
            self._auth_metrics_service.inc_login_failure()
            raise

        self._auth_metrics_service.inc_login_success()
        return LoginResult(
            access_token=access_token,
            refresh_token=refresh_token,
        )
