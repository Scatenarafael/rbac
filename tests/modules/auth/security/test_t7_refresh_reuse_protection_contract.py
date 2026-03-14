from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[4]
REFRESH_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/refresh_session_usecase.py"


def test_t7_refresh_usecase_file_exists() -> None:
    if not REFRESH_USECASE_FILE.exists():
        pytest.fail("Arquivo esperado não encontrado: src/modules/auth/application/usecases/refresh_session_usecase.py")


def test_t7_refresh_usecase_has_reuse_detection_flow() -> None:
    source = REFRESH_USECASE_FILE.read_text().lower()
    assert "reuse" in source or "reused" in source, (
        "F7 deve detectar reuse de refresh token e tratá-lo explicitamente."
    )


def test_t7_refresh_usecase_revokes_sessions_on_reuse() -> None:
    source = REFRESH_USECASE_FILE.read_text()
    assert "list_by_user_id" in source, (
        "F7 deve consultar sessões do usuário para revogação em massa após detecção de reuse."
    )
    assert "revoke" in source, (
        "F7 deve revogar sessão atual e/ou cadeia de sessões após detecção de reuse."
    )
