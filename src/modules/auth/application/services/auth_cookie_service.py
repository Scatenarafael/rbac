from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi import Response

from src.core.config.config import Settings, get_settings
from src.modules.auth.domain.exceptions import ValidationError


class AuthCookieService:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._validate_cookie_security()

    def set_access_cookie(self, response: Response, token: str) -> None:
        expires_at = datetime.now(UTC) + timedelta(minutes=self._settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        response.set_cookie(
            key=self._settings.ACCESS_COOKIE_NAME,
            value=token,
            httponly=self._settings.COOKIE_HTTPONLY,
            secure=self._settings.COOKIE_SECURE,
            samesite=self._cookie_samesite(),
            max_age=self._settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            expires=expires_at,
            domain=self._settings.COOKIE_DOMAIN,
            path="/",
        )

    def set_refresh_cookie(self, response: Response, token: str) -> None:
        expires_at = datetime.now(UTC) + timedelta(days=self._settings.REFRESH_TOKEN_EXPIRE_DAYS)
        response.set_cookie(
            key=self._settings.REFRESH_COOKIE_NAME,
            value=token,
            httponly=self._settings.COOKIE_HTTPONLY,
            secure=self._settings.COOKIE_SECURE,
            samesite=self._cookie_samesite(),
            max_age=self._settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            expires=expires_at,
            domain=self._settings.COOKIE_DOMAIN,
            path="/",
        )

    def clear_auth_cookies(self, response: Response) -> None:
        response.delete_cookie(
            key=self._settings.ACCESS_COOKIE_NAME,
            path="/",
            secure=self._settings.COOKIE_SECURE,
            samesite=self._cookie_samesite(),
            domain=self._settings.COOKIE_DOMAIN,
        )
        response.delete_cookie(
            key=self._settings.REFRESH_COOKIE_NAME,
            path="/",
            secure=self._settings.COOKIE_SECURE,
            samesite=self._cookie_samesite(),
            domain=self._settings.COOKIE_DOMAIN,
        )

    def _cookie_samesite(self) -> str:
        return self._settings.COOKIE_SAMESITE or "lax"

    def _validate_cookie_security(self) -> None:
        if self._cookie_samesite().lower() == "none" and not self._settings.COOKIE_SECURE:
            raise ValidationError("COOKIE_SECURE must be true when COOKIE_SAMESITE is 'none'.")
