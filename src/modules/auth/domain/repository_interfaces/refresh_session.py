from abc import abstractmethod
from uuid import UUID

from src.modules.auth.domain.entities.refresh_session import RefreshSession
from src.modules.auth.domain.repository_interfaces.repository_base import IRepositoryBase


class IRefreshSessionRepository(IRepositoryBase[RefreshSession, UUID]):
    @abstractmethod
    async def get_by_jti(self, jti: str) -> RefreshSession | None:
        pass

    @abstractmethod
    async def list_by_user_id(self, user_id: UUID) -> list[RefreshSession]:
        pass
