"""Mocked model catalogue for phenotype prediction."""

from __future__ import annotations

from typing import List

from typing_extensions import TypedDict


class MockModel(TypedDict):
    """Representation of a phenotype prediction model."""

    id: str
    display_name: str
    version: str
    description: str
    supported_inputs: List[str]
    predictable_phenotypes: List[str]


MOCK_MODELS: List[MockModel] = [
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
