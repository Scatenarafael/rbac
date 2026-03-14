from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
COOKIE_SERVICE_FILE = PROJECT_ROOT / "src/modules/auth/application/services/auth_cookie_service.py"


def test_t7_cookie_service_file_exists() -> None:
    if not COOKIE_SERVICE_FILE.exists():
        pytest.fail("Arquivo esperado não encontrado: src/modules/auth/application/services/auth_cookie_service.py")


def test_t7_cookie_service_sets_expires_and_domain() -> None:
    source = COOKIE_SERVICE_FILE.read_text().lower()
    assert "expires" in source, "F7 deve explicitar `expires` em cookies de auth."
    assert "domain" in source, "F7 deve parametrizar `domain` para política de cookie em produção."


def test_t7_cookie_service_enforces_secure_in_production_flow() -> None:
    source = COOKIE_SERVICE_FILE.read_text().lower()
    assert "secure" in source
    assert "cookie_secure" in source
    assert "validationerror" in source or "raise" in source, (
        "F7 deve ter proteção contra configuração insegura de cookie em cenários sensíveis."
    )
