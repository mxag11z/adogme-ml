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

    async def get_by_service_id(self, dog_service_id: str) -> DogEntity | None:
        statement = select(DogEntity).where(DogEntity.dog_service_id == dog_service_id)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def update_dog(self, dog: DogEntity) -> DogEntity:
        db_dog = await self.get_by_service_id(dog.dog_service_id)
        if not db_dog:
            raise ValueError(f"Dog with service id {dog.dog_service_id} not found")
        
        dog_data = dog.model_dump(exclude_unset=True, exclude={"id"})
        for key, value in dog_data.items():
            setattr(db_dog, key, value)
            
        self.session.add(db_dog)
        await self.session.commit()
        await self.session.refresh(db_dog)
        return db_dog

    async def delete_dog(self, dog_id: str) -> bool:
        statement = select(DogEntity).where(DogEntity.dog_service_id == dog_id)
        result = await self.session.execute(statement)
        dog = result.scalars().first()
        if not dog:
            return False
        await self.session.delete(dog)
        await self.session.commit()
        return True
