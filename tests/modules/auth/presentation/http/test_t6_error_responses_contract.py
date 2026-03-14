from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
AUTH_ROUTER_FILE = PROJECT_ROOT / "src/modules/auth/presentation/http/routers/auth_router.py"


def test_t6_router_declares_401_403_responses() -> None:
    source = AUTH_ROUTER_FILE.read_text()
    assert "responses" in source, (
        "F6 deve declarar responses 401/403 nos endpoints protegidos para contrato HTTP explícito."
    )
    assert "401" in source
    assert "403" in source


def test_t6_router_handles_auth_errors_without_500() -> None:
    source = AUTH_ROUTER_FILE.read_text()
    assert "HTTPException" in source or "ValidationError" in source, (
        "F6 deve mapear erros de autenticação/autorização sem cair em 500 genérico."
    )
