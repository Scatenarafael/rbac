from __future__ import annotations

from uuid import UUID

from src.modules.auth.application.services.auth_metrics_service import AuthMetricsService
from src.modules.auth.domain.repository_interfaces.refresh_session import IRefreshSessionRepository


class LogoutAllUseCase:
    def __init__(
        self,
        refresh_session_repository: IRefreshSessionRepository,
        auth_metrics_service: AuthMetricsService | None = None,
    ) -> None:
        self._refresh_session_repository = refresh_session_repository
        self._auth_metrics_service = auth_metrics_service or AuthMetricsService()

    async def execute(self, *, user_id: UUID) -> int:
        sessions = await self._refresh_session_repository.list_by_user_id(user_id)
        revoked_count = 0

        for session in sessions:
            if session.is_revoked:
                continue
            session.revoke()
            await self._refresh_session_repository.update(session.id, session)
            revoked_count += 1

        self._auth_metrics_service.inc_logout_all()
        return revoked_count
