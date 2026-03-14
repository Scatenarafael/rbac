from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
FINGERPRINT_FILE = PROJECT_ROOT / "src/modules/auth/application/services/session_fingerprint.py"


def test_t7_session_fingerprint_file_exists() -> None:
    if not FINGERPRINT_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/application/services/session_fingerprint.py")


def test_t7_session_fingerprint_contract() -> None:
    if not FINGERPRINT_FILE.exists():
        pytest.fail("SessionFingerprintService ainda não implementado para validar contrato.")

    source = FINGERPRINT_FILE.read_text()
    assert "class SessionFingerprintService" in source
    assert "def build_fingerprint" in source
    assert "user_agent" in source
    assert "ip_address" in source
