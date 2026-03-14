from __future__ import annotations

from src.modules.auth.domain.exceptions import ValidationError
from src.modules.auth.domain.repository_interfaces.refresh_session import IRefreshSessionRepository


class LogoutUseCase:
    def __init__(self, refresh_session_repository: IRefreshSessionRepository) -> None:
        self._refresh_session_repository = refresh_session_repository

    async def execute(self, *, refresh_token_jti: str) -> None:
        jti = refresh_token_jti.strip()
        if not jti:
            raise ValidationError("Refresh token jti cannot be empty.")

        session = await self._refresh_session_repository.get_by_jti(jti)
        if session is None:
            return

        session.revoke()
        await self._refresh_session_repository.update(session.id, session)
