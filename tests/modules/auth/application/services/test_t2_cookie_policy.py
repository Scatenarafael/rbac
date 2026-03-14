from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
COOKIE_SERVICE_FILE = PROJECT_ROOT / "src/modules/auth/application/services/auth_cookie_service.py"


def test_t2_auth_cookie_service_file_exists() -> None:
    if not COOKIE_SERVICE_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/application/services/auth_cookie_service.py")


def test_t2_auth_cookie_service_contract() -> None:
    if not COOKIE_SERVICE_FILE.exists():
        pytest.fail("AuthCookieService ainda não implementado para validar contrato.")

    source = COOKIE_SERVICE_FILE.read_text()
    assert "class AuthCookieService" in source
    assert "def set_access_cookie" in source
    assert "def set_refresh_cookie" in source
    assert "def clear_auth_cookies" in source


def test_t2_auth_cookie_service_enforces_http_only_policy() -> None:
    if not COOKIE_SERVICE_FILE.exists():
        pytest.fail("AuthCookieService ainda não implementado para validar política de cookie.")

    source = COOKIE_SERVICE_FILE.read_text().lower()
    for keyword in ["httponly", "secure", "samesite"]:
        assert keyword in source, f"AuthCookieService deve aplicar política `{keyword}`."
