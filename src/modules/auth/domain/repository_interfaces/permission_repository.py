from uuid import UUID

from src.modules.auth.domain.entities.permission import Permission
from src.modules.auth.domain.repository_interfaces.repository_base import IRepositoryBase


class IPermissionRepository(IRepositoryBase[Permission, UUID]):
    pass
