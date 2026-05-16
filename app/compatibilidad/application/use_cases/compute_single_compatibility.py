from dataclasses import dataclass

from ...domain.repositories.dog_repository import DogRepository
from .compute_compatibility import compute_similarity


@dataclass
class SingleCompatibilityResult:
    compatibility_score: float
    user_vector: list[float]
    dog_vector: list[float]


class ComputeSingleCompatibility:
    def __init__(self, dog_repo: DogRepository, alpha: float = 0.6, beta: float = 0.4):
        self.dog_repo = dog_repo
        self.alpha = alpha
        self.beta = beta

    async def execute(self, dog_service_id: str, user_vector: list[float]) -> SingleCompatibilityResult | None:
        dog = await self.dog_repo.get_by_service_id(dog_service_id)
        if dog is None or not dog.dog_vector or dog.AdoptionSpeed is None:
            return None

        similarity = compute_similarity(user_vector, dog.dog_vector)
        ml_score = round(1.0 - (dog.AdoptionSpeed / 3.0), 4)
        compatibility_score = round(self.alpha * similarity + self.beta * ml_score, 4)

        return SingleCompatibilityResult(
            compatibility_score=compatibility_score,
            user_vector=user_vector,
            dog_vector=dog.dog_vector,
        )
