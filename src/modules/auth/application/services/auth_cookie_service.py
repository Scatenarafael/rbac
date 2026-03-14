from __future__ import annotations

from fastapi import Response

from src.core.config.config import Settings, get_settings


class AuthCookieService:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    def set_access_cookie(self, response: Response, token: str) -> None:
        response.set_cookie(
            key=self._settings.ACCESS_COOKIE_NAME,
            value=token,
            httponly=self._settings.COOKIE_HTTPONLY,
            secure=self._settings.COOKIE_SECURE,
            samesite=self._cookie_samesite(),
            max_age=self._settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
        )

    def set_refresh_cookie(self, response: Response, token: str) -> None:
        response.set_cookie(
            key=self._settings.REFRESH_COOKIE_NAME,
            value=token,
            httponly=self._settings.COOKIE_HTTPONLY,
            secure=self._settings.COOKIE_SECURE,
            samesite=self._cookie_samesite(),
            max_age=self._settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            path="/",
        )

    def clear_auth_cookies(self, response: Response) -> None:
        response.delete_cookie(
            key=self._settings.ACCESS_COOKIE_NAME,
            path="/",
            secure=self._settings.COOKIE_SECURE,
            samesite=self._cookie_samesite(),
        )
        response.delete_cookie(
            key=self._settings.REFRESH_COOKIE_NAME,
            path="/",
            secure=self._settings.COOKIE_SECURE,
            samesite=self._cookie_samesite(),
        )

    def _cookie_samesite(self) -> str:
        return self._settings.COOKIE_SAMESITE or "lax"
