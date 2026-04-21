from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODEL_PATH: str = "./adoption_model.pkl"
    CONFIG_PATH: str = "./model_config.json"
    ALPHA: float = 0.6
    BETA: float = 0.4
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    # DATABASE_URL: str = "postgresql+asyncpg://adogme_user:adogme_pass@localhost:5432/adogme"
    DATABASE_URL: str = "postgresql+asyncpg://189a52a4b521ff3d20b1851835196395652d7b43ddd3c7728434f6ce76b0dc2c:sk_ouv3ia8CMl69ShUlBKizc@db.prisma.io:5432/postgres?ssl=require"

    class Config:
        env_file = ".env"
settings = Settings()
