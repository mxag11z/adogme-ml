from ...domain.entities.compatibility_result import GeneralInsightsResult, GeneralInsight
from ...domain.repositories.prediction_repository import PredictionRepository

# Features that shelters can actually influence, mapped to actionable recommendations.
ACTIONABLE_FEATURES: dict[str, str] = {
    "PhotoAmt": "Agregar más fotos al perfil del perro",
    "VideoAmt": "Incluir videos del perro en el perfil",
    "has_photos": "Asegurarse de que el perfil tenga al menos una foto",
    "has_video": "Asegurarse de que el perfil tenga al menos un video",
    "has_name": "Asignar un nombre al perro",
    "Fee": "Considerar ajustar la cuota de adopción",
    "is_free": "Considerar ofrecer adopción gratuita",
    "desc_length": "Escribir una descripción más detallada del perro",
    "desc_word_count": "Ampliar la descripción con más información relevante",
    "Vaccinated": "Vacunar al perro y registrarlo en el perfil",
    "Dewormed": "Desparasitar al perro y registrarlo en el perfil",
    "Sterilized": "Esterilizar al perro y registrarlo en el perfil",
    "health_score": "Completar el cuadro médico (vacunas, desparasitación, esterilización)",
}


class GetDogRecommendations:
    def __init__(self, prediction_repo: PredictionRepository):
        self.prediction_repo = prediction_repo

    def execute(self) -> GeneralInsightsResult:
        importances = self.prediction_repo.get_feature_importances()
        sorted_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)

        insights: list[GeneralInsight] = []
        for rank, (feature, importance) in enumerate(sorted_features, start=1):
            if feature in ACTIONABLE_FEATURES:
                insights.append(GeneralInsight(
                    feature=feature,
                    importance=round(importance, 4),
                    rank=rank,
                    recommendation=ACTIONABLE_FEATURES[feature],
                ))

        return GeneralInsightsResult(
            total_features=len(importances),
            actionable_insights=insights,
        )
