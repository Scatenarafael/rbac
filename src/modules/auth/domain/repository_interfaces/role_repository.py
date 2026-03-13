from uuid import UUID

from src.modules.auth.domain.entities.role import Role
from src.modules.auth.domain.repository_interfaces.repository_base import IRepositoryBase


class IRoleRepository(IRepositoryBase[Role, UUID]):
    pass
