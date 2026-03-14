from __future__ import annotations

import hashlib
import hmac
import secrets
from uuid import uuid4

from src.modules.auth.domain.exceptions import ValidationError


class RefreshTokenSecurity:
    def hash_refresh_token(self, refresh_token: str) -> str:
        token = refresh_token.strip()
        if not token:
            raise ValidationError("Refresh token cannot be empty.")
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def verify_refresh_token(self, refresh_token: str, token_hash: str) -> bool:
        token = refresh_token.strip()
        hashed = token_hash.strip()
        if not token:
            raise ValidationError("Refresh token cannot be empty.")
        if not hashed:
            raise ValidationError("Refresh token hash cannot be empty.")

        candidate_hash = self.hash_refresh_token(token)
        return hmac.compare_digest(candidate_hash, hashed)

    def generate_token_jti(self) -> str:
        return uuid4().hex

    def generate_refresh_token(self) -> str:
        return secrets.token_urlsafe(64)
