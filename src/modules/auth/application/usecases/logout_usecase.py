from __future__ import annotations

from src.modules.auth.application.services.auth_metrics_service import AuthMetricsService
from src.modules.auth.domain.exceptions import ValidationError
from src.modules.auth.domain.repository_interfaces.refresh_session import IRefreshSessionRepository


class LogoutUseCase:
    def __init__(
        self,
        refresh_session_repository: IRefreshSessionRepository,
        auth_metrics_service: AuthMetricsService | None = None,
    ) -> None:
        self._refresh_session_repository = refresh_session_repository
        self._auth_metrics_service = auth_metrics_service or AuthMetricsService()

    async def execute(self, *, refresh_token_jti: str) -> None:
        jti = refresh_token_jti.strip()
        if not jti:
            raise ValidationError("Refresh token jti cannot be empty.")

        session = await self._refresh_session_repository.get_by_jti(jti)
        if session is None:
            self._auth_metrics_service.inc_logout()
            return

        session.revoke()
        await self._refresh_session_repository.update(session.id, session)
        self._auth_metrics_service.inc_logout()
