from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class UserTenantRoleModel(SQLModel, table=True):
    __tablename__ = "user_tenant_roles"
    __table_args__ = (
        UniqueConstraint("user_id", "tenant_id", "role_id", name="uq_user_tenant_roles_user_tenant_role"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
    role_id: UUID = Field(foreign_key="roles.id", index=True)
