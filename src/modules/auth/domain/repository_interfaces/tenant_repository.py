from uuid import UUID

from src.modules.auth.domain.entities.tenant import Tenant
from src.modules.auth.domain.repository_interfaces.repository_base import IRepositoryBase


class ITenantRepository(IRepositoryBase[Tenant, UUID]):
    pass
