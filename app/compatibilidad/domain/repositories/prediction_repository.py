from abc import ABC, abstractmethod
from ..entities.dog_entity import DogEntity


class PredictionRepository(ABC):
    @abstractmethod
    def predict_proba(self, dog: DogEntity) -> list[float]:
        """Regresa lista de 5 probabilidades [P(speed0), ..., P(speed4)]."""
        pass

    @abstractmethod
    def get_feature_importances(self) -> dict[str, float]:
        """Regresa diccionario mapeando nombre de feature a valor de importancia."""
        pass

