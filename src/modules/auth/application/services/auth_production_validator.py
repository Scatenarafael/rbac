from __future__ import annotations

from dataclasses import dataclass

from src.core.config.config import Settings, get_settings
from src.modules.auth.domain.exceptions import ValidationError

DEFAULT_INSECURE_SECRETS = {
    "",
    "change-me-super-secret",
}


@dataclass(slots=True)
class AuthProductionValidator:
    settings: Settings | None = None

    def __post_init__(self) -> None:
        if self.settings is None:
            self.settings = get_settings()

    def validate(self) -> None:
        assert self.settings is not None
        current_settings = self.settings

        if current_settings.SECRET_KEY.strip() in DEFAULT_INSECURE_SECRETS:
            raise ValidationError("SECRET_KEY inseguro para produção.")

        if current_settings.ACCESS_SECRET.strip() in DEFAULT_INSECURE_SECRETS:
            raise ValidationError("ACCESS_SECRET inseguro para produção.")

        if not current_settings.COOKIE_SECURE:
            raise ValidationError("COOKIE_SECURE deve ser true em produção.")

        samesite = (current_settings.COOKIE_SAMESITE or "").lower()
        if samesite not in {"lax", "strict", "none"}:
            raise ValidationError("COOKIE_SAMESITE inválido.")

        if samesite == "none" and not current_settings.COOKIE_SECURE:
            raise ValidationError("COOKIE_SECURE deve ser true quando COOKIE_SAMESITE='none'.")

        if not current_settings.COOKIE_DOMAIN:
            raise ValidationError("COOKIE_DOMAIN deve ser definido em produção.")
