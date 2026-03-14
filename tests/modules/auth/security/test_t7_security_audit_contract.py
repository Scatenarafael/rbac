from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
SECURITY_AUDIT_FILE = PROJECT_ROOT / "src/modules/auth/application/services/security_audit_service.py"


def test_t7_security_audit_service_file_exists() -> None:
    if not SECURITY_AUDIT_FILE.exists():
        pytest.fail(
            "Arquivo esperado ainda não implementado: src/modules/auth/application/services/security_audit_service.py"
        )


def test_t7_security_audit_service_contract() -> None:
    if not SECURITY_AUDIT_FILE.exists():
        pytest.fail("SecurityAuditService ainda não implementado para validar contrato.")

    source = SECURITY_AUDIT_FILE.read_text()
    assert "class SecurityAuditService" in source
    assert "def log_login_success" in source
    assert "def log_login_failure" in source
    assert "def log_refresh_reuse_detected" in source
    assert "def log_logout_all" in source
