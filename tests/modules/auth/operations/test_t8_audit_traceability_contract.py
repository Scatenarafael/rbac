from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
SECURITY_AUDIT_FILE = PROJECT_ROOT / "src/modules/auth/application/services/security_audit_service.py"


def test_t8_security_audit_service_file_exists() -> None:
    if not SECURITY_AUDIT_FILE.exists():
        pytest.fail("Arquivo esperado não encontrado: src/modules/auth/application/services/security_audit_service.py")


def test_t8_security_audit_service_includes_correlation_context() -> None:
    source = SECURITY_AUDIT_FILE.read_text()
    lowered = source.lower()

    assert "request_id" in lowered, (
        "F8 deve incluir request_id nos eventos críticos de auditoria para rastreabilidade operacional."
    )
    assert "user_id" in lowered, (
        "F8 deve incluir user_id (quando disponível) nos eventos críticos de auditoria."
    )


def test_t8_security_audit_service_contract_for_critical_events() -> None:
    source = SECURITY_AUDIT_FILE.read_text()
    assert "def log_login_success" in source
    assert "def log_login_failure" in source
    assert "def log_refresh_reuse_detected" in source
    assert "def log_logout_all" in source
