from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
ALEMBIC_VERSIONS_DIR = PROJECT_ROOT / "alembic" / "versions"


def test_t1_auth_migration_file_exists() -> None:
    migration_files = sorted(ALEMBIC_VERSIONS_DIR.glob("*.py"))
    if not migration_files:
        pytest.fail("Nenhuma migração encontrada em alembic/versions para iniciar F1.")


def test_t1_auth_migration_creates_auth_tables() -> None:
    migration_files = sorted(ALEMBIC_VERSIONS_DIR.glob("*.py"))
    if not migration_files:
        pytest.fail("Nenhuma migração encontrada em alembic/versions para validação de tabelas.")

    source = migration_files[-1].read_text()
    expected_tables = [
        "users",
        "tenants",
        "roles",
        "permissions",
        "role_permissions",
        "user_tenant_roles",
        "refresh_sessions",
    ]

    for table_name in expected_tables:
        assert table_name in source, (
            f"Migração de auth deve criar/gerenciar tabela `{table_name}`."
        )
