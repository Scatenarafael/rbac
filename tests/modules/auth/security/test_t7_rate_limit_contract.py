from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
RATE_LIMITER_FILE = PROJECT_ROOT / "src/modules/auth/application/services/auth_rate_limiter.py"


def test_t7_auth_rate_limiter_file_exists() -> None:
    if not RATE_LIMITER_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/application/services/auth_rate_limiter.py")


def test_t7_auth_rate_limiter_contract() -> None:
    if not RATE_LIMITER_FILE.exists():
        pytest.fail("AuthRateLimiter ainda não implementado para validar contrato.")

    source = RATE_LIMITER_FILE.read_text()
    assert "class AuthRateLimiter" in source
    assert "def check_login_attempt" in source
    assert "def register_failed_attempt" in source
    assert "def reset_attempts" in source
