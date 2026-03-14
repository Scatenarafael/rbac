from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from src.modules.auth.domain.exceptions import ValidationError


@dataclass(slots=True)
class AuthRateLimiter:
    max_attempts: int = 5
    window_seconds: int = 300

    def __post_init__(self) -> None:
        self._attempts: dict[str, list[datetime]] = {}

    def check_login_attempt(self, identity: str) -> None:
        key = identity.strip().lower()
        now = datetime.now(UTC)
        attempts = self._attempts.get(key, [])
        valid_since = now - timedelta(seconds=self.window_seconds)
        recent_attempts = [attempt for attempt in attempts if attempt >= valid_since]
        self._attempts[key] = recent_attempts

        if len(recent_attempts) >= self.max_attempts:
            raise ValidationError("Too many login attempts. Please try again later.")

    def register_failed_attempt(self, identity: str) -> None:
        key = identity.strip().lower()
        now = datetime.now(UTC)
        self._attempts.setdefault(key, []).append(now)

    def reset_attempts(self, identity: str) -> None:
        key = identity.strip().lower()
        self._attempts.pop(key, None)
