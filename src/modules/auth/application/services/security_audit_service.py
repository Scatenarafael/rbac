from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.core.logging.ports import LoggerPort


@dataclass(slots=True)
class SecurityAuditService:
    logger: LoggerPort | None = None

    def _emit(self, level: str, event: str, **fields: Any) -> None:
        if self.logger is None:
            return
        handler = getattr(self.logger, level, None)
        if callable(handler):
            handler(event, **fields)

    def log_login_success(self, *, user_id: str, ip_address: str | None = None) -> None:
        self._emit("info", "auth.login.success", user_id=user_id, ip_address=ip_address)

    def log_login_failure(self, *, email: str, ip_address: str | None = None) -> None:
        self._emit("warning", "auth.login.failure", email=email, ip_address=ip_address)

    def log_refresh_reuse_detected(self, *, user_id: str, token_jti: str) -> None:
        self._emit("warning", "auth.refresh.reuse_detected", user_id=user_id, token_jti=token_jti)

    def log_logout_all(self, *, user_id: str, revoked_count: int) -> None:
        self._emit("info", "auth.logout_all", user_id=user_id, revoked_count=revoked_count)
