"""Service layer for phenotype model discovery."""

from __future__ import annotations

from typing import List

from app.data.mock_models import MOCK_MODELS, MockModel


def list_available_models() -> List[MockModel]:
    """Return all available phenotype prediction models.

    The data is currently served from a mocked catalogue while the
    persistent model registry is under development.
    """

    return MOCK_MODELS


def list_model_phenotypes(model_id: str) -> List[str]:
    """Return predictable phenotypes for the requested model.

    Args:
        model_id: Identifier of the phenotype model.

    Returns:
        A list of phenotype identifiers that the model can predict.

    Raises:
        KeyError: If the model identifier is unknown.
    """

    for model in MOCK_MODELS:
        if model["id"] == model_id:
            return list(model.get("predictable_phenotypes", []))
    raise KeyError(model_id)
