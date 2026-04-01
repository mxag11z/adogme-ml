import json
from contextlib import asynccontextmanager

import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .compatibilidad.infrastructure.routers.compatibility_router import router as compatibility_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load(settings.MODEL_PATH)
    with open(settings.CONFIG_PATH) as f:
        app.state.config = json.load(f)

    app.state.feature_cols = app.state.config["feature_columns"]
    app.state.alpha = settings.ALPHA
    app.state.beta = settings.BETA

    print(f"Model loaded: {settings.MODEL_PATH}")
    print(f"Features: {len(app.state.feature_cols)}")
    yield


app = FastAPI(
    title="aDOGme ML Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(compatibility_router)
