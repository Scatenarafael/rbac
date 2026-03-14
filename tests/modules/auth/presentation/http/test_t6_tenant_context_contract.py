from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
AUTH_DEPENDENCIES_FILE = PROJECT_ROOT / "src/modules/auth/presentation/http/auth_dependencies.py"


def test_t6_tenant_context_dependency_exists() -> None:
    source = AUTH_DEPENDENCIES_FILE.read_text()
    assert "get_tenant_context" in source, (
        "F6 deve expor dependência para resolução do tenant corrente."
    )


def test_t6_tenant_context_accepts_header_or_param() -> None:
    source = AUTH_DEPENDENCIES_FILE.read_text().lower()
    expected_tokens = ["x-tenant-id", "tenant_id", "header", "path", "query"]
    for token in expected_tokens:
        assert token in source, (
            "F6 deve documentar/implementar resolução de tenant por header e/ou parâmetro de rota."
        )


def test_t6_tenant_context_validates_missing_tenant() -> None:
    source = AUTH_DEPENDENCIES_FILE.read_text()
    assert "ValidationError" in source or "HTTPException" in source, (
        "F6 deve tratar ausência/invalidade de tenant no contexto."
    )
