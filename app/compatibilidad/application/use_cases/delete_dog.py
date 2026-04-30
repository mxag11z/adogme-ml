from ...domain.repositories.dog_repository import DogRepository

class DeleteDog:
    """Receives a dog id from the CRUD microservice, deletes the dog."""

    def __init__(self, dog_repo: DogRepository):
        self.dog_repo = dog_repo

    async def execute(self, dog_id: str) -> bool:
        return await self.dog_repo.delete_dog(dog_id)
