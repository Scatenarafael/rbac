from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
PERMISSION_EVALUATOR_FILE = PROJECT_ROOT / "src/modules/auth/application/services/permission_evaluator.py"


def test_t4_permission_evaluator_service_file_exists() -> None:
    if not PERMISSION_EVALUATOR_FILE.exists():
        pytest.fail("Arquivo esperado ainda não implementado: src/modules/auth/application/services/permission_evaluator.py")


def test_t4_permission_evaluator_service_contract() -> None:
    if not PERMISSION_EVALUATOR_FILE.exists():
        pytest.fail("PermissionEvaluator ainda não implementado para validar contrato.")

    source = PERMISSION_EVALUATOR_FILE.read_text()
    assert "class PermissionEvaluator" in source
    assert "def has_permission" in source
    assert "permission_code" in source
    assert "PermissionCode" in source
