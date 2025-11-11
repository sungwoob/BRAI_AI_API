"""Service layer for phenotype model discovery."""

from __future__ import annotations

from typing import List

from app.data.ai_models import (
    AI_MODELS,
    AIModel,
    OptionalAIModelFields,
    RequiredAIModelFields,
    add_ai_model,
    remove_ai_model,
)


def list_available_models() -> List[AIModel]:
    """Return all available phenotype prediction models.

    The data is currently served from a mocked catalogue while the
    persistent model registry is under development.
    """

    return AI_MODELS


def list_model_phenotypes(model_id: str) -> List[str]:
    """Return predictable phenotypes for the requested model.

    Args:
        model_id: Identifier of the phenotype model.

    Returns:
        A list of phenotype identifiers that the model can predict.

    Raises:
        KeyError: If the model identifier is unknown.
    """

    for model in AI_MODELS:
        if model["id"] == model_id:
            return list(model.get("predictable_phenotypes", []))
    raise KeyError(model_id)


def register_model(
    *, required: RequiredAIModelFields, optional: OptionalAIModelFields | None = None
) -> AIModel:
    """Add a new model to the catalogue."""

    return add_ai_model(required=required, optional=optional)


def unregister_model(model_id: str) -> AIModel:
    """Remove a model from the catalogue by identifier."""

    return remove_ai_model(model_id)
