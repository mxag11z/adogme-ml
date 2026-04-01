from __future__ import annotations
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.dog_entity import DogEntity
from ..domain.repositories.dog_repository import DogRepository


class DbDogRepository(DogRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[DogEntity]:
        result = await self.session.execute(text("SELECT * FROM dogs"))
        rows = result.mappings().all()
        return [DogEntity(**row) for row in rows]
