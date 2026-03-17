from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.core.logging.context import get_request_id, get_user_id
from src.core.logging.ports import LoggerPort


@dataclass(slots=True)
class SecurityAuditService:
    logger: LoggerPort | None = None

    def _emit(self, level: str, event: str, **fields: Any) -> None:
        request_id = get_request_id()
        context_user_id = get_user_id()
        if request_id is not None:
            fields["request_id"] = request_id
        if context_user_id is not None and "user_id" not in fields:
            fields["user_id"] = context_user_id

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
