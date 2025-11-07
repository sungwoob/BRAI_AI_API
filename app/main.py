"""FastAPI application exposing phenotype model discovery endpoints."""

from __future__ import annotations

from typing import List

from fastapi import FastAPI

from app.data.mock_models import MockModel
from app.services.model_catalog import list_available_models

app = FastAPI(
    title="BRAI Phenotype Prediction API",
    description=(
        "API endpoints for interacting with phenotype prediction models."
        "\n\n"
        "The current implementation exposes mocked catalogue data to support "
        "early integration of the inference workflow."
    ),
    version="0.1.0",
)


@app.get("/api/models", response_model=List[MockModel])
async def get_available_models() -> List[MockModel]:
    """Retrieve the list of available phenotype prediction models."""

    return list_available_models()
