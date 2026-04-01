from typing import Optional
from pydantic import BaseModel, Field
import numpy as np


class UserAnswerEntity(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    user_vector: Optional[list[float]] = None
    q1: int = Field(..., ge=1, le=5)
    q2: int = Field(..., ge=1, le=5)
    q3: int = Field(..., ge=1, le=5)
    q4: int = Field(..., ge=1, le=5)
    q5: int = Field(..., ge=1, le=5)
    q6: int = Field(..., ge=1, le=5)
    q7: int = Field(..., ge=1, le=5)
    q8: int = Field(..., ge=1, le=5)
    q9: int = Field(..., ge=1, le=5)
    q10: int = Field(..., ge=1, le=5)
    q11: int = Field(..., ge=1, le=5)
    q12: int = Field(..., ge=1, le=5)
    q13: int = Field(..., ge=1, le=5)
    q14: int = Field(..., ge=1, le=5)
    q15: int = Field(..., ge=1, le=5)
    q16: int = Field(..., ge=1, le=5)
    q17: int = Field(..., ge=1, le=5)
    q18: int = Field(..., ge=1, le=5)
    q19: int = Field(..., ge=1, le=5)
    q20: int = Field(..., ge=1, le=5)


## user to vector mapping: activity (q1-q5), housing (q6-q10), experience (q11-q15), care (q16-q20)
    def to_vector(self) -> list[float]:
        """Mapeamos las respuestas a un vector de 4 dimensiones: [activity, housing, experience, care]."""
        answers = self.model_dump()
        ##obtenemos el promedio de cada bloque de preguntas.
        activity = float(np.mean([answers[f"q{i}"] for i in range(1, 6)]))
        housing = float(np.mean([answers[f"q{i}"] for i in range(6, 11)]))
        experience = float(np.mean([answers[f"q{i}"] for i in range(11, 16)]))
        care = float(np.mean([answers[f"q{i}"] for i in range(16, 21)]))
        return [activity, housing, experience, care]
