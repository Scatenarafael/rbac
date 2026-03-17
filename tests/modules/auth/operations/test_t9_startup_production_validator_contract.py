from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
APP_FACTORY_FILE = PROJECT_ROOT / "src/core/http/app_factory.py"


def _non_comment_lines(source: str) -> list[str]:
    return [line.strip() for line in source.splitlines() if line.strip() and not line.strip().startswith("#")]


def test_t9_app_factory_file_exists() -> None:
    if not APP_FACTORY_FILE.exists():
        pytest.fail("Arquivo esperado não encontrado: src/core/http/app_factory.py")


def test_t9_app_factory_imports_auth_production_validator() -> None:
    source = APP_FACTORY_FILE.read_text()
    active_lines = _non_comment_lines(source)
    assert any("AuthProductionValidator" in line and "import" in line for line in active_lines), (
        "F9 deve importar AuthProductionValidator no app_factory para validação operacional em startup."
    )


def test_t9_app_factory_validates_production_auth_configuration_on_startup() -> None:
    source = APP_FACTORY_FILE.read_text()
    active_lines = _non_comment_lines(source)

    assert any("create_app" in line for line in active_lines), "Contrato exige create_app ativo no app_factory."
    assert any("AuthProductionValidator" in line for line in active_lines), (
        "F9 deve instanciar AuthProductionValidator durante bootstrap da aplicação."
    )
    assert any("validate(" in line and "AuthProductionValidator" in line for line in active_lines) or any(
        "validate(" in line and "validator" in line.lower() for line in active_lines
    ), "F9 deve executar validate() para bloquear startup com configuração insegura."
