from __future__ import annotations
from abc import ABC, abstractmethod
from ..entities.dog_entity import DogEntity

##Unico abstract method ya que solo necesitamos obtener la lista de perros para el ranking de compatibilidad. El procesamiento individual de cada perro se hace en el use case ProcessDog, que también se apoya en PredictionRepository para obtener insights y vectorizar al perro.
class DogRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[DogEntity]:
        pass
