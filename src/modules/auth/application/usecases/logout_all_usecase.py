from __future__ import annotations

from uuid import UUID

from src.modules.auth.domain.repository_interfaces.refresh_session import IRefreshSessionRepository


class LogoutAllUseCase:
    def __init__(self, refresh_session_repository: IRefreshSessionRepository) -> None:
        self._refresh_session_repository = refresh_session_repository

    async def execute(self, *, user_id: UUID) -> int:
        sessions = await self._refresh_session_repository.list_by_user_id(user_id)
        revoked_count = 0

        for session in sessions:
            if session.is_revoked:
                continue
            session.revoke()
            await self._refresh_session_repository.update(session.id, session)
            revoked_count += 1

        return revoked_count
