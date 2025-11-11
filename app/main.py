"""FastAPI application exposing phenotype model discovery endpoints."""

from __future__ import annotations

from typing import List

from fastapi import FastAPI, HTTPException

from app.data.ai_models import AIModel
from app.services.model_catalog import list_available_models, list_model_phenotypes

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


@app.get("/api/models", response_model=List[AIModel])
async def get_available_models() -> List[AIModel]:
    """Retrieve the list of available phenotype prediction models."""

    return list_available_models()


@app.get("/api/models/{model_id}/phenotypes", response_model=List[str])
async def get_model_phenotypes(model_id: str) -> List[str]:
    """Return the phenotypes that the requested model can predict."""

    try:
        return list_model_phenotypes(model_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Model not found") from exc
