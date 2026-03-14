from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]


def require_file(relative_path: str) -> Path:
    file_path = PROJECT_ROOT / relative_path
    if not file_path.exists():
        pytest.fail(f"Arquivo esperado ainda não implementado: {relative_path}")
    return file_path

REQUIRED_MAPPER_FILES = [
    "src/modules/auth/infrastructure/mappers/user_mapper.py",
    "src/modules/auth/infrastructure/mappers/tenant_mapper.py",
    "src/modules/auth/infrastructure/mappers/role_mapper.py",
    "src/modules/auth/infrastructure/mappers/permission_mapper.py",
    "src/modules/auth/infrastructure/mappers/refresh_session_mapper.py",
]


def test_t1_required_mapper_files_exist() -> None:
    for relative_path in REQUIRED_MAPPER_FILES:
        require_file(relative_path)


def test_t1_mappers_define_to_model_and_to_domain_contract() -> None:
    for relative_path in REQUIRED_MAPPER_FILES:
        source = require_file(relative_path).read_text()
        assert "to_model" in source, f"{relative_path} deve expor conversão para modelo."
        assert "to_domain" in source, f"{relative_path} deve expor conversão para domínio."
