from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from jose import JWTError, jwt

from src.core.config.config import Settings, get_settings
from src.modules.auth.domain.exceptions import ValidationError


class JWTService:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    def create_access_token(
        self,
        *,
        subject: str,
        tenant_id: str | None = None,
        additional_claims: dict[str, Any] | None = None,
        expires_delta: timedelta | None = None,
    ) -> str:
        claims: dict[str, Any] = dict(additional_claims or {})
        now = datetime.now(timezone.utc)
        expiration = now + (expires_delta or timedelta(minutes=self._settings.ACCESS_TOKEN_EXPIRE_MINUTES))

        claims.update(
            {
                "sub": subject,
                "jti": uuid4().hex,
                "type": "access",
                "tenant_id": tenant_id,
                "iat": now,
                "exp": expiration,
            }
        )
        return jwt.encode(claims, self._settings.SECRET_KEY, algorithm=self._settings.ALGORITHM)

    def create_refresh_token(
        self,
        *,
        subject: str,
        tenant_id: str | None = None,
        additional_claims: dict[str, Any] | None = None,
        expires_delta: timedelta | None = None,
    ) -> str:
        claims: dict[str, Any] = dict(additional_claims or {})
        now = datetime.now(timezone.utc)
        expiration = now + (expires_delta or timedelta(days=self._settings.REFRESH_TOKEN_EXPIRE_DAYS))

        claims.update(
            {
                "sub": subject,
                "jti": uuid4().hex,
                "type": "refresh",
                "tenant_id": tenant_id,
                "iat": now,
                "exp": expiration,
            }
        )
        return jwt.encode(claims, self._settings.SECRET_KEY, algorithm=self._settings.ALGORITHM)

    def decode_token(
        self,
        token: str,
        *,
        expected_type: str | None = None,
    ) -> dict[str, Any]:
        raw_token = token.strip()
        if not raw_token:
            raise ValidationError("Token cannot be empty.")

        try:
            payload = jwt.decode(
                raw_token,
                self._settings.SECRET_KEY,
                algorithms=[self._settings.ALGORITHM],
            )
        except JWTError as exc:
            raise ValidationError("Invalid token.") from exc

        if expected_type is not None and payload.get("type") != expected_type:
            raise ValidationError(f"Unexpected token type: {payload.get('type')}")

        return payload
