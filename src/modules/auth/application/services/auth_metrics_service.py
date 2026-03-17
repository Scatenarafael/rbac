from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AuthMetricsService:
    """
    In-memory counters for auth/authorization operational metrics.
    """

    _counters: dict[str, int] = field(default_factory=dict)

    def _inc(self, metric: str, value: int = 1) -> None:
        self._counters[metric] = self._counters.get(metric, 0) + value

    def inc_login_success(self) -> None:
        self._inc("auth.login.success")

    def inc_login_failure(self) -> None:
        self._inc("auth.login.failure")

    def inc_refresh_success(self) -> None:
        self._inc("auth.refresh.success")

    def inc_refresh_failure(self) -> None:
        self._inc("auth.refresh.failure")

    def inc_refresh_reuse_detected(self) -> None:
        self._inc("auth.refresh.reuse_detected")

    def inc_logout(self) -> None:
        self._inc("auth.logout")

    def inc_logout_all(self) -> None:
        self._inc("auth.logout_all")

    def snapshot(self) -> dict[str, int]:
        return dict(self._counters)
