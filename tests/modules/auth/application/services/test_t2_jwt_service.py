from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
JWT_SERVICE_FILE = PROJECT_ROOT / "src/modules/auth/application/services/jwt_service.py"


def test_t2_jwt_service_file_exists() -> None:
    if not JWT_SERVICE_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/application/services/jwt_service.py")


def test_t2_jwt_service_contract() -> None:
    if not JWT_SERVICE_FILE.exists():
        pytest.fail("JWTService ainda não implementado para validar contrato.")

    source = JWT_SERVICE_FILE.read_text()
    assert "class JWTService" in source
    assert "def create_access_token" in source
    assert "def create_refresh_token" in source
    assert "def decode_token" in source


def test_t2_jwt_service_expected_claims_are_handled() -> None:
    if not JWT_SERVICE_FILE.exists():
        pytest.fail("JWTService ainda não implementado para validar claims.")

    source = JWT_SERVICE_FILE.read_text()
    for claim in ["sub", "jti", "exp", "type", "tenant_id"]:
        assert claim in source, f"JWTService deve lidar com claim `{claim}`."
