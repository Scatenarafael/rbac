import src.modules.auth.domain.repository_interfaces as repository_interfaces


def test_refresh_session_repository_is_package_export() -> None:
    assert hasattr(repository_interfaces, "IRefreshSessionRepository"), (
        "IRefreshSessionRepository precisa ser reexportado em "
        "repository_interfaces/__init__.py."
    )
    assert "IRefreshSessionRepository" in repository_interfaces.__all__
