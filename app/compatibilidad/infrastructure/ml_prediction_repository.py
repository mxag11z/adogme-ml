import pandas as pd
from ..domain.entities.dog_entity import DogEntity
from ..domain.repositories.prediction_repository import PredictionRepository


class MlPredictionRepository(PredictionRepository):
    """Implements PredictionRepository using sklearn model + pandas feature engineering."""

    def __init__(self, model, feature_cols: list[str]):
        self.model = model
        self.feature_cols = feature_cols
        self.importances = dict(zip(feature_cols, model.feature_importances_))

    def predict_proba(self, dog: DogEntity) -> list[float]:
        features_df = self._to_features_df(dog)
        probs = self.model.predict_proba(features_df[self.feature_cols])[0]
        return [round(float(p), 4) for p in probs]

    def get_feature_importances(self) -> dict[str, float]:
        return self.importances

    def get_feature_values(self, dog: DogEntity) -> dict[str, float]:
        features_df = self._to_features_df(dog)
        return features_df.iloc[0].to_dict()

    def _to_features_df(self, dog: DogEntity) -> pd.DataFrame:
        """Convert DogEntity to DataFrame with 23 features the model expects."""
        desc = dog.Description or ""
        return pd.DataFrame([{
            "Age": dog.Age,
            "Breed1": dog.Breed1,
            "Gender": dog.Gender,
            "MaturitySize": dog.MaturitySize,
            "FurLength": dog.FurLength,
            "Vaccinated": dog.Vaccinated,
            "Dewormed": dog.Dewormed,
            "Sterilized": dog.Sterilized,
            "Health": dog.Health,
            "Quantity": dog.Quantity,
            "Fee": dog.Fee,
            "PhotoAmt": dog.PhotoAmt,
            "VideoAmt": dog.VideoAmt,
            "is_mixed_breed": 1 if dog.is_mixed_breed() else 0,
            "has_name": 1 if dog.Name else 0,
            "is_puppy": 1 if dog.is_puppy() else 0,
            "is_free": 1 if dog.Fee == 0 else 0,
            "desc_length": len(desc),
            "desc_word_count": len(desc.split()) if desc else 0,
            "health_score": dog.health_score(),
            "age_bucket": (
                0 if dog.Age <= 3 else
                1 if dog.Age <= 12 else
                2 if dog.Age <= 48 else 3
            ),
            "has_photos": 1 if dog.PhotoAmt > 0 else 0,
            "has_video": 1 if dog.VideoAmt > 0 else 0,
        }])
