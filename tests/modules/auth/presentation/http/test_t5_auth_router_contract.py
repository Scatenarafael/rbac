from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
AUTH_ROUTER_FILE = PROJECT_ROOT / "src/modules/auth/presentation/http/routers/auth_router.py"


def test_t5_auth_router_file_exists() -> None:
    if not AUTH_ROUTER_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/presentation/http/routers/auth_router.py")


def test_t5_auth_router_contract() -> None:
    if not AUTH_ROUTER_FILE.exists():
        pytest.fail("Auth router ainda não implementado para validar contrato.")

    source = AUTH_ROUTER_FILE.read_text()
    assert "APIRouter" in source
    assert "router = APIRouter" in source
    assert "Depends" in source


def test_t5_auth_router_exposes_expected_endpoints() -> None:
    if not AUTH_ROUTER_FILE.exists():
        pytest.fail("Auth router ainda não implementado para validar endpoints.")

    source = AUTH_ROUTER_FILE.read_text()
    expected_paths = [
        "register",
        "login",
        "refresh",
        "logout",
        "logout-all",
        "me",
    ]
    for expected_path in expected_paths:
        assert expected_path in source, f"Router deve expor endpoint relacionado a `{expected_path}`."
