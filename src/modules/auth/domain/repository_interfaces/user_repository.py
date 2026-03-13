from abc import abstractmethod
from uuid import UUID

from src.modules.auth.domain.entities.user import User
from src.modules.auth.domain.repository_interfaces.repository_base import IRepositoryBase
from src.modules.auth.domain.value_objects.emails import Email


class IUserRepository(IRepositoryBase[User, UUID]):
    @abstractmethod
    async def get_by_email(self, email: Email) -> User | None:
        pass
