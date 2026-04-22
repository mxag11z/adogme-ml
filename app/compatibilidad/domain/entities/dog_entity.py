from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Float
from sqlalchemy.dialects.postgresql import ARRAY
from typing import Optional
import numpy as np


class DogEntity(SQLModel, table=True):
    __tablename__ = "dogs"
    __table_args__ = {"schema": "ml_service"}
    id: Optional[int] = Field(default=None, primary_key=True)
    dog_service_id: str = Field(index=True, unique=True, description="ID reference from Main Dog Microservice")
    Name: Optional[str] = None
    Age: int = Field(..., ge=0, description="Age in months")
    Breed1: int
    Breed2: int = 0
    Gender: int = Field(..., ge=1, le=3)
    MaturitySize: int = Field(..., ge=1, le=4)
    FurLength: int = Field(..., ge=1, le=3)
    Vaccinated: int = Field(..., ge=1, le=3)
    Dewormed: int = Field(..., ge=1, le=3)
    Sterilized: int = Field(..., ge=1, le=3)
    Health: int = Field(..., ge=1, le=3)
    Quantity: int = 1
    Fee: int = Field(0, ge=0)
    PhotoAmt: int = Field(0, ge=0)
    VideoAmt: int = Field(0, ge=0)
    Description: str = ""
    AdoptionSpeed: Optional[int] = Field(None, ge=0, le=3)
    dog_vector: Optional[list[float]] = Field(default=None, sa_column=Column(ARRAY(Float)))

    def is_mixed_breed(self) -> bool:
        return self.Breed2 != 0 or self.Breed1 == 307 or self.Breed2 == 307

    def is_puppy(self) -> bool:
        return self.Age <= 3

    def health_score(self) -> int:
        return (
            (1 if self.Vaccinated == 1 else 0)
            + (1 if self.Dewormed == 1 else 0)
            + (1 if self.Sterilized == 1 else 0)
        )

    def to_vector(self) -> list[float]:
        """Mapeamos dog a un vector de 4 dimensiones: [activity, space, training, care]."""
        age = self.Age

        age_activity = 5.0 if age <= 6 else (4.0 if age <= 24 else (3.0 if age <= 84 else 2.0))
        size_activity = {1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0}.get(self.MaturitySize, 3.0)
        activity_req = (age_activity + size_activity) / 2

        space_req = {1: 1.5, 2: 2.5, 3: 3.5, 4: 5.0}.get(self.MaturitySize, 3.0)

        age_train = 5.0 if age <= 6 else (4.0 if age <= 12 else (3.0 if age <= 48 else 2.0))
        health_train = {1: 1.0, 2: 3.0, 3: 5.0}.get(self.Health, 2.0)
        training_diff = (age_train + health_train) / 2

        health_base = {1: 1.0, 2: 3.0, 3: 5.0}.get(self.Health, 2.0)
        medical_need = 5.0 - self.health_score() * (4.0 / 3.0)
        care_req = (health_base + medical_need) / 2

        return [activity_req, space_req, training_diff, care_req]
