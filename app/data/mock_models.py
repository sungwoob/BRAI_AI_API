"""Mocked model catalogue for phenotype prediction."""

from __future__ import annotations

from typing import List, TypedDict


class MockModel(TypedDict):
    """Representation of a phenotype prediction model."""

    id: str
    display_name: str
    version: str
    description: str
    supported_inputs: List[str]


MOCK_MODELS: List[MockModel] = [
    {
        "id": "phenotype_classifier_v1",
        "display_name": "Phenotype Classifier",
        "version": "1.0.0",
        "description": "Logistic regression model trained on genotype features.",
        "supported_inputs": ["genotype_variants", "patient_metadata"],
    },
    {
        "id": "phenotype_transformer_beta",
        "display_name": "Phenotype Transformer",
        "version": "0.9.2-beta",
        "description": "Transformer network for phenotype sequence prediction.",
        "supported_inputs": ["gene_expression", "clinical_notes"],
    },
    {
        "id": "phenotype_gnn_experimental",
        "display_name": "Phenotype Graph Network",
        "version": "0.2.1",
        "description": "Graph neural network leveraging protein interaction graphs.",
        "supported_inputs": ["protein_interactions", "genomic_variants"],
    },
]
