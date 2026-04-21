import numpy as np

from ...domain.entities.dog_entity import DogEntity
from ...domain.repositories.prediction_repository import PredictionRepository
from ...domain.repositories.dog_repository import DogRepository

SPEED_LABELS = {
    0: "Primeros 7 dias",
    1: "8-30 dias",
    2: "31-90 dias",
    3: "No adoptado",
}


class ProcessDogResult:
    def __init__(self, adoption_speed: int, speed_label: str, dog_vector: list[float]):
        self.adoption_speed = adoption_speed
        self.speed_label = speed_label
        self.dog_vector = dog_vector


class ProcessDog:
    """Receives a dog from the CRUD microservice, computes AdoptionSpeed + dog_vector, returns them."""

    def __init__(self, prediction_repo: PredictionRepository, dog_repo: DogRepository):
        self.prediction_repo = prediction_repo
        self.dog_repo = dog_repo

    async def execute(self, dog: DogEntity) -> ProcessDogResult:
        probs = self.prediction_repo.predict_proba(dog)
        adoption_speed = int(np.argmax(probs))
        dog_vector = dog.to_vector()

        dog.AdoptionSpeed = adoption_speed
        dog.dog_vector = dog_vector

        await self.dog_repo.create_dog(dog)

        return ProcessDogResult(
            adoption_speed=adoption_speed,
            speed_label=SPEED_LABELS[adoption_speed],
            dog_vector=dog_vector,
        )
