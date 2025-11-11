"""Mocked AI model catalogue for phenotype prediction."""

from __future__ import annotations

from typing import List

from typing_extensions import TypedDict


class RequiredAIModelFields(TypedDict):
    """Required fields that every AI model entry must provide."""

    id: str
    display_name: str
    version: str
    supported_inputs: List[str]
    predictable_phenotypes: List[str]


class OptionalAIModelFields(TypedDict, total=False):
    """Optional metadata that can accompany an AI model entry."""

    description: str


class AIModel(RequiredAIModelFields, OptionalAIModelFields):
    """Representation of a phenotype prediction model."""


AI_MODELS: List[AIModel] = [
    {
        "id": "phenotype_classifier_v1",
        "display_name": "Phenotype Classifier",
        "version": "1.0.0",
        "description": "Logistic regression model trained on genotype features.",
        "supported_inputs": ["genotype_variants", "patient_metadata"],
        "predictable_phenotypes": [
            "diabetes_risk",
            "cardiovascular_event_probability",
            "metabolic_syndrome_indicator",
        ],
    },
    {
        "id": "phenotype_transformer_beta",
        "display_name": "Phenotype Transformer",
        "version": "0.9.2-beta",
        "description": "Transformer network for phenotype sequence prediction.",
        "supported_inputs": ["gene_expression", "clinical_notes"],
        "predictable_phenotypes": [
            "disease_progression_stage",
            "treatment_response_category",
            "rare_disorder_likelihood",
        ],
    },
    {
        "id": "phenotype_gnn_experimental",
        "display_name": "Phenotype Graph Network",
        "version": "0.2.1",
        "description": "Graph neural network leveraging protein interaction graphs.",
        "supported_inputs": ["protein_interactions", "genomic_variants"],
        "predictable_phenotypes": [
            "tumor_invasiveness_score",
            "immune_response_profile",
        ],
    },
]


def add_ai_model(*, required: RequiredAIModelFields, optional: OptionalAIModelFields | None = None) -> AIModel:
    """Add a new AI model entry to the in-memory catalogue.

    Args:
        required: Mandatory fields describing the model.
        optional: Optional metadata that augments the required fields.

    Returns:
        The combined AI model entry that was inserted.

    Raises:
        ValueError: If a model with the same identifier already exists.
    """

    model_id = required["id"]
    if any(existing["id"] == model_id for existing in AI_MODELS):
        raise ValueError(f"Model with id '{model_id}' already exists")

    model: AIModel = {**required, **(optional or {})}
    AI_MODELS.append(model)
    return model


def remove_ai_model(model_id: str) -> AIModel:
    """Remove an AI model entry from the in-memory catalogue.

    Args:
        model_id: Identifier of the model to remove.

    Returns:
        The removed AI model entry.

    Raises:
        KeyError: If no model with the provided identifier exists.
    """

    for index, model in enumerate(AI_MODELS):
        if model["id"] == model_id:
            return AI_MODELS.pop(index)

    raise KeyError(model_id)

