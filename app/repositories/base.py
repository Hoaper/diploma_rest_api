from typing import Generic, TypeVar, Optional, List
from abc import ABC, abstractmethod

T = TypeVar('T')

class BaseRepository(Generic[T], ABC):
    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        pass

    @abstractmethod
    async def update(self, entity_id: str, entity: T) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        pass 