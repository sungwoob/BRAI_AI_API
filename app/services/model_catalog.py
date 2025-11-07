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
