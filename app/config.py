from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODEL_PATH: str = "./adoption_model.pkl"
    CONFIG_PATH: str = "./model_config.json"
    ALPHA: float = 0.6
    BETA: float = 0.4
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DATABASE_URL: str = "postgresql+asyncpg://adogme_user:adogme_pass@localhost:5432/adogme"

    class Config:
        env_file = ".env"
settings = Settings()
