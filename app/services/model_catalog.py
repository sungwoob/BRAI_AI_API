"""Service layer for phenotype model discovery and predictions."""

from __future__ import annotations

import random
from typing import List, Sequence

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


def phenotype_prediction(model_id: str, genotype_data: Sequence[str]) -> float:
    """Produce a mocked phenotype prediction score for a model.

    Args:
        model_id: Identifier of the phenotype model that should perform the
            prediction.
        genotype_data: Genotype values that would normally be fed into the
            underlying model. The mock implementation ignores the actual values
            but keeps the signature aligned with the expected inference call.

    Returns:
        A floating-point score between 0.0 and 1.0 representing the predicted
        phenotype likelihood.

    Raises:
        KeyError: If the model identifier does not exist in the catalogue.
        ValueError: If no genotype information was supplied.
    """

    if not genotype_data:
        raise ValueError("Genotype data must not be empty for prediction")

    for model in AI_MODELS:
        if model["id"] == model_id:
            return random.random()

    raise KeyError(model_id)
