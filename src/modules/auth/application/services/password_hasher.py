from __future__ import annotations

from passlib.context import CryptContext

from src.modules.auth.domain.exceptions import ValidationError


class PasswordHasher:
    def __init__(self) -> None:
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, plain_password: str) -> str:
        password = plain_password.strip()
        if not password:
            raise ValidationError("Password cannot be empty.")
        return self._pwd_context.hash(password)

    def verify_password(self, plain_password: str, password_hash: str) -> bool:
        password = plain_password.strip()
        hashed = password_hash.strip()
        if not password:
            raise ValidationError("Password cannot be empty.")
        if not hashed:
            raise ValidationError("Password hash cannot be empty.")
        return self._pwd_context.verify(password, hashed)
