import inspect

from src.modules.auth.domain.repository_interfaces.refresh_session import IRefreshSessionRepository
from src.modules.auth.domain.repository_interfaces.repository_base import IRepositoryBase
from src.modules.auth.domain.repository_interfaces.user_repository import IUserRepository


def test_repository_base_constructor_should_not_require_infrastructure_session() -> None:
    signature = inspect.signature(IRepositoryBase.__init__)
    non_self_params = [name for name in signature.parameters if name != "self"]
    assert non_self_params == [], (
        "IRepositoryBase não deve exigir AsyncSession no construtor; "
        "esse acoplamento de infra será resolvido na fase F0."
    )


def test_user_repository_get_by_email_must_be_async() -> None:
    assert inspect.iscoroutinefunction(IUserRepository.get_by_email), (
        "IUserRepository.get_by_email deve ser async para manter consistência "
        "com os demais contratos assíncronos."
    )


def test_refresh_session_repository_get_by_jti_is_async() -> None:
    assert inspect.iscoroutinefunction(IRefreshSessionRepository.get_by_jti)
