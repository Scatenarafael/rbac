from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
AUTH_METRICS_FILE = PROJECT_ROOT / "src/modules/auth/application/services/auth_metrics_service.py"


def test_t8_auth_metrics_service_file_exists() -> None:
    if not AUTH_METRICS_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/application/services/auth_metrics_service.py")


def test_t8_auth_metrics_service_contract() -> None:
    if not AUTH_METRICS_FILE.exists():
        pytest.fail("AuthMetricsService ainda não implementado para validar contrato.")

    source = AUTH_METRICS_FILE.read_text()
    assert "class AuthMetricsService" in source
    assert "def inc_login_success" in source
    assert "def inc_login_failure" in source
    assert "def inc_refresh_success" in source
    assert "def inc_refresh_failure" in source
    assert "def inc_refresh_reuse_detected" in source
    assert "def inc_logout" in source
    assert "def inc_logout_all" in source
