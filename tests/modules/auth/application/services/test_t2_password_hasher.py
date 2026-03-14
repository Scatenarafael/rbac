from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
PASSWORD_HASHER_FILE = PROJECT_ROOT / "src/modules/auth/application/services/password_hasher.py"


def test_t2_password_hasher_file_exists() -> None:
    if not PASSWORD_HASHER_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/application/services/password_hasher.py")


def test_t2_password_hasher_contract() -> None:
    if not PASSWORD_HASHER_FILE.exists():
        pytest.fail("PasswordHasher ainda não implementado para validar contrato.")

    source = PASSWORD_HASHER_FILE.read_text()
    assert "class PasswordHasher" in source
    assert "def hash_password" in source
    assert "def verify_password" in source
