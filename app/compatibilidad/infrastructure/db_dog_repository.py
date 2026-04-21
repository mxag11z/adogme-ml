from __future__ import annotations
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.dog_entity import DogEntity
from ..domain.repositories.dog_repository import DogRepository


class DbDogRepository(DogRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[DogEntity]:
        result = await self.session.execute(select(DogEntity))
        return list(result.scalars().all())

    async def create_dog(self, dog: DogEntity) -> DogEntity:
        self.session.add(dog)
        await self.session.commit()
        await self.session.refresh(dog)
        return dog
