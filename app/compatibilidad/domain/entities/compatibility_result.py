from __future__ import annotations
from pydantic import BaseModel


class CompatibilityResult(BaseModel):
    dog_id: int
    dog_service_id: str
    compatibility_score: float
    similarity: float
    ml_score: float
    user_vector: list[float]
    dog_vector: list[float]
    predicted_speed: int
    speed_label: str
    probabilities: dict[str, float]


class CompatibilityRankingResult(BaseModel):
    top_n: int
    results: list[CompatibilityResult]


class GeneralInsight(BaseModel):
    feature: str
    importance: float
    rank: int
    recommendation: str


class GeneralInsightsResult(BaseModel):
    total_features: int
    actionable_insights: list[GeneralInsight]
