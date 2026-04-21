from fastapi import APIRouter, Request, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.dog_entity import DogEntity
from ...domain.entities.user_answer_entity import UserAnswerEntity
from ...domain.entities.compatibility_result import (
    CompatibilityRankingResult,
    GeneralInsightsResult,
)
from ...domain.repositories.dog_repository import DogRepository
from ...domain.repositories.prediction_repository import PredictionRepository
from ...application.use_cases.compute_compatibility import ComputeCompatibility
from ...application.use_cases.process_dog import ProcessDog
from ...application.use_cases.process_questionnaire import ProcessQuestionnaire
from ...application.use_cases.get_dog_recommendations import GetDogRecommendations
from ...infrastructure.ml_prediction_repository import MlPredictionRepository
from ...infrastructure.db_dog_repository import DbDogRepository
from ....database import get_session


router = APIRouter()


# -- Dependency providers --

async def get_dog_repo(session: AsyncSession = Depends(get_session)) -> DogRepository:
    return DbDogRepository(session)


def get_ml_repo(request: Request) -> PredictionRepository:
    return MlPredictionRepository(request.app.state.model, request.app.state.feature_cols)


# -- Request bodies --

class RankingRequest(BaseModel):
    user_vector: list[float] = Field(..., min_length=4, max_length=4)


# -- Endpoints --

@router.get("/health")
async def health_check(request: Request):
    return {
        "status": "healthy",
        "model_loaded": request.app.state.model is not None,
        "model_type": request.app.state.config.get("model_type", "unknown"),
        "n_features": len(request.app.state.feature_cols),
    }


@router.post("/predict/process-dog")
async def process_dog(
    dog: DogEntity, 
    ml_repo: PredictionRepository = Depends(get_ml_repo),
    dog_repo: DogRepository = Depends(get_dog_repo)
):
    """Called by CRUD microservice when a dog is created/updated.
    Returns adoption_speed + dog_vector for the CRUD service to persist."""
    use_case = ProcessDog(ml_repo, dog_repo)
    result = await use_case.execute(dog)
    return {
        "adoption_speed": result.adoption_speed,
        "speed_label": result.speed_label,
        "dog_vector": result.dog_vector,
    }


@router.post("/predict/process-questionnaire")
async def process_questionnaire(answers: UserAnswerEntity):
    """Called by backend when a user completes the questionnaire.
    Returns user_vector for the backend to persist."""
    use_case = ProcessQuestionnaire()
    user_vector = use_case.execute(answers)
    return {
        "user_vector": user_vector,
    }


@router.post("/predict/compatible-dogs", response_model=CompatibilityRankingResult)
async def compatible_dogs(
    body: RankingRequest,
    request: Request,
    top_n: int = Query(10, ge=1, le=100),
    dog_repo: DogRepository = Depends(get_dog_repo),
):
    """Called by backend after questionnaire. Receives user_vector,
    reads all dogs from DB (read-only), returns ranked compatibility."""
    use_case = ComputeCompatibility(dog_repo, request.app.state.alpha, request.app.state.beta)
    return await use_case.execute(body.user_vector, top_n)


@router.get("/insights/general-recommendations", response_model=GeneralInsightsResult)
async def general_recommendations(ml_repo: PredictionRepository = Depends(get_ml_repo)):
    use_case = GetDogRecommendations(ml_repo)
    return use_case.execute()
