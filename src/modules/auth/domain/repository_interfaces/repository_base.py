from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TEntity = TypeVar("TEntity")
TId = TypeVar("TId")


class IRepositoryBase(ABC, Generic[TEntity, TId]):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    async def create(self, data: TEntity) -> TEntity:
        pass

    @abstractmethod
    async def get_by_id(self, id: TId) -> TEntity | None:
        pass

    @abstractmethod
    async def update(self, id: TId, data: TEntity) -> TEntity | None:
        pass

    @abstractmethod
    async def delete(self, id: TId) -> bool:
        pass
