"""FastAPI application exposing phenotype model discovery endpoints."""

from __future__ import annotations

from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.data.ai_models import AIModel, OptionalAIModelFields, RequiredAIModelFields
from app.services.model_catalog import (
    list_available_models,
    list_model_phenotypes,
    register_model,
    unregister_model,
)

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


class CreateAIModelPayload(BaseModel):
    """Request body for registering a new AI model."""

    id: str
    display_name: str
    version: str
    supported_inputs: List[str]
    predictable_phenotypes: List[str]
    description: str | None = None

    def split_required_optional(self) -> tuple[RequiredAIModelFields, OptionalAIModelFields | None]:
        required: RequiredAIModelFields = {
            "id": self.id,
            "display_name": self.display_name,
            "version": self.version,
            "supported_inputs": list(self.supported_inputs),
            "predictable_phenotypes": list(self.predictable_phenotypes),
        }
        optional: OptionalAIModelFields = {}
        if self.description is not None:
            optional["description"] = self.description
        return required, optional or None


@app.post("/api/models", response_model=AIModel, status_code=201)
async def create_ai_model(payload: CreateAIModelPayload) -> AIModel:
    """Register a new AI model in the catalogue."""

    required, optional = payload.split_required_optional()
    try:
        return register_model(required=required, optional=optional)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.delete("/api/models/{model_id}", response_model=AIModel)
async def delete_ai_model(model_id: str) -> AIModel:
    """Remove an AI model from the catalogue."""

    try:
        return unregister_model(model_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Model not found") from exc
