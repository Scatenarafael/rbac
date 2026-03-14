from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
REFRESH_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/refresh_session_usecase.py"
REFRESH_REPOSITORY_FILE = (
    PROJECT_ROOT / "src/modules/auth/infrastructure/repositories/refresh_session_repository_sqlmodel.py"
)


def test_t7_refresh_concurrency_guards_are_present() -> None:
    usecase_source = REFRESH_USECASE_FILE.read_text().lower()
    repository_source = REFRESH_REPOSITORY_FILE.read_text().lower()

    has_lock_strategy = any(
        token in usecase_source or token in repository_source
        for token in ["lock", "with_for_update", "select_for_update", "transaction"]
    )
    assert has_lock_strategy, (
        "F7 deve incluir estratégia de concorrência para evitar refresh duplo simultâneo."
    )


def test_t7_refresh_concurrency_uses_idempotent_rotation_marker() -> None:
    source = REFRESH_USECASE_FILE.read_text().lower()
    assert "replaced_by_token_jti" in source, (
        "F7 deve usar marcador de rotação para garantir idempotência e rastreabilidade."
    )
