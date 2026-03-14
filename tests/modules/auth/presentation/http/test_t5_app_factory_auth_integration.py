from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
APP_FACTORY_FILE = PROJECT_ROOT / "src/core/http/app_factory.py"


def _non_comment_lines(source: str) -> list[str]:
    return [line.strip() for line in source.splitlines() if line.strip() and not line.strip().startswith("#")]


def test_t5_app_factory_file_exists() -> None:
    if not APP_FACTORY_FILE.exists():
        pytest.fail("Arquivo esperado não encontrado: src/core/http/app_factory.py")


def test_t5_app_factory_imports_auth_router() -> None:
    source = APP_FACTORY_FILE.read_text()
    active_lines = _non_comment_lines(source)
    assert any("import" in line and "auth_router" in line for line in active_lines), (
        "app_factory deve importar o router de auth de forma ativa (não comentada)."
    )


def test_t5_app_factory_includes_auth_router() -> None:
    source = APP_FACTORY_FILE.read_text()
    active_lines = _non_comment_lines(source)
    assert any("include_router" in line and "auth_router" in line for line in active_lines), (
        "create_app deve incluir o router de auth."
    )
