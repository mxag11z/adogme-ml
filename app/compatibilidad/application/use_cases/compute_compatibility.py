import numpy as np

from ...domain.entities.dog_entity import DogEntity
from ...domain.entities.compatibility_result import CompatibilityResult, CompatibilityRankingResult
from ...domain.repositories.dog_repository import DogRepository

SPEED_LABELS = {
    0: "Primeros 7 dias",
    1: "8-30 dias",
    2: "31-90 dias",
    3: "No adoptado",
}

class ComputeCompatibility:
    def __init__(self, dog_repo: DogRepository, alpha: float = 0.6, beta: float = 0.4):
        self.dog_repo = dog_repo
        self.alpha = alpha
        self.beta = beta

    async def execute(self, user_vector: list[float], top_n: int = 10) -> CompatibilityRankingResult:
        dogs = await self.dog_repo.get_all()
        ##lista con la entidad resultado de compatibilidad
        results: list[CompatibilityResult] = []
        for dog in dogs:
            if not dog.dog_vector or dog.AdoptionSpeed is None:
                continue

            ##estamos comparando el vector del usuario con el vector del perro, con cada perro en la base de datos.
            similarity = self._compute_similarity(user_vector, dog.dog_vector)

            # Normalizamos, la adoption speed es inversamente proporcional a la compatibilidad, por eso restamos de 1.0
            ml_score = round(1.0 - (dog.AdoptionSpeed / 3.0), 4)

            ##computamos la compatibilidad como se definio en un inicio, combinacion lineal de similitud y score del modelo ML, con pesos alpha y beta respectivamente.
            compatibility_score = round(self.alpha * similarity + self.beta * ml_score, 4)

            results.append(CompatibilityResult(
                dog_id=dog.id,
                dog_service_id=dog.dog_service_id,
                compatibility_score=compatibility_score,
                similarity=similarity,
                ml_score=ml_score,
                user_vector=user_vector,
                dog_vector=dog.dog_vector,
                predicted_speed=dog.AdoptionSpeed,
                speed_label=SPEED_LABELS.get(dog.AdoptionSpeed, "Desconocido"),
                probabilities={},
            ))

        ##Se ordena basado en el compatibility_score
        results.sort(key=lambda r: r.compatibility_score, reverse=True)

        ##Segun el top_n solicitado se devuelve esa lista.
        return CompatibilityRankingResult(
            top_n=top_n,
            results=results[:top_n],
        )

    def _compute_similarity(self, user_vector: list[float], dog_vector: list[float]) -> float:
        """Calcula la similitud usando distancia euclidiana asimetrica.

        Solo penaliza cuando el perro requiere MAS de lo que el usuario ofrece.
        Si el usuario tiene de mas (sobre-cualificado) no penaliza, ya que eso
        no genera incompatibilidad real en una adopcion."""
        user_arr = np.array(user_vector)
        dog_arr = np.array(dog_vector)
        # Solo cuenta la diferencia cuando dog > user (perro requiere mas que el usuario)
        deficits = np.maximum(0.0, dog_arr - user_arr)
        distance = np.sqrt(np.sum(deficits ** 2))
        max_distance = np.sqrt(4 * (5 - 1) ** 2)  # = 8.0
        similarity = 1.0 - (distance / max_distance)
        return round(max(0.0, float(similarity)), 4)
