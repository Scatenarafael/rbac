from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[5]
LOGIN_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/login_usecase.py"
REFRESH_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/refresh_session_usecase.py"
LOGOUT_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/logout_usecase.py"
LOGOUT_ALL_USECASE_FILE = PROJECT_ROOT / "src/modules/auth/application/usecases/logout_all_usecase.py"


def _assert_file_exists(path: Path) -> None:
    if not path.exists():
        pytest.fail(f"Arquivo esperado não encontrado: {path.as_posix()}")


def test_t9_auth_usecases_files_exist() -> None:
    _assert_file_exists(LOGIN_USECASE_FILE)
    _assert_file_exists(REFRESH_USECASE_FILE)
    _assert_file_exists(LOGOUT_USECASE_FILE)
    _assert_file_exists(LOGOUT_ALL_USECASE_FILE)


def test_t9_login_usecase_emits_auth_metrics_contract() -> None:
    source = LOGIN_USECASE_FILE.read_text()
    assert "AuthMetricsService" in source, (
        "F9 deve injetar AuthMetricsService no LoginUseCase."
    )
    assert "inc_login_success" in source, (
        "F9 deve registrar métrica de sucesso no login."
    )
    assert "inc_login_failure" in source, (
        "F9 deve registrar métrica de falha no login."
    )


def test_t9_refresh_usecase_emits_auth_metrics_contract() -> None:
    source = REFRESH_USECASE_FILE.read_text()
    assert "AuthMetricsService" in source, (
        "F9 deve injetar AuthMetricsService no RefreshSessionUseCase."
    )
    assert "inc_refresh_success" in source, (
        "F9 deve registrar métrica de sucesso no refresh."
    )
    assert "inc_refresh_failure" in source, (
        "F9 deve registrar métrica de falha no refresh."
    )
    assert "inc_refresh_reuse_detected" in source, (
        "F9 deve registrar métrica para detecção de reuse no refresh token."
    )


def test_t9_logout_usecase_emits_auth_metrics_contract() -> None:
    source = LOGOUT_USECASE_FILE.read_text()
    assert "AuthMetricsService" in source, (
        "F9 deve injetar AuthMetricsService no LogoutUseCase."
    )
    assert "inc_logout" in source, (
        "F9 deve registrar métrica de logout."
    )


def test_t9_logout_all_usecase_emits_auth_metrics_contract() -> None:
    source = LOGOUT_ALL_USECASE_FILE.read_text()
    assert "AuthMetricsService" in source, (
        "F9 deve injetar AuthMetricsService no LogoutAllUseCase."
    )
    assert "inc_logout_all" in source, (
        "F9 deve registrar métrica de logout-all."
    )
