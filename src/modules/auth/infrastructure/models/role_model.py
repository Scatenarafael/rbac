from __future__ import annotations

from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class RoleModel(SQLModel, table=True):
    __tablename__ = "roles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True, max_length=255)
    description: str | None = Field(default=None, max_length=1024)
