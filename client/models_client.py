"""Simple client for interacting with the phenotype prediction API."""

from __future__ import annotations

import csv
from argparse import ArgumentParser
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Iterable, List, Sequence

import httpx


class PhenotypeApiClient(AbstractContextManager["PhenotypeApiClient"]):
    """Client for querying the phenotype prediction API."""

    def __init__(self, base_url: str = "http://localhost:8000", *, timeout: float = 10.0) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def list_models(self) -> List[dict]:
        """Return the available models from the API."""

        response = self._client.get("/api/models")
        response.raise_for_status()
        data: Sequence[dict] = response.json()
        return list(data)

    def list_model_phenotypes(self, model_id: str) -> List[str]:
        """Return phenotypes that the specified model can predict."""

        response = self._client.get(f"/api/models/{model_id}/phenotypes")
        response.raise_for_status()
        data: Sequence[str] = response.json()
        return list(data)

    def register_model(self, model_payload: dict) -> dict:
        """Register a model in the catalogue via the API."""

        response = self._client.post("/api/models", json=model_payload)
        response.raise_for_status()
        return response.json()

    def delete_model(self, model_id: str) -> dict:
        """Remove a model from the catalogue via the API."""

        response = self._client.delete(f"/api/models/{model_id}")
        response.raise_for_status()
        return response.json()

    def phenotype_prediction(self, model_id: str, genotype_data: Sequence[str]) -> dict:
        """Request a phenotype prediction for the provided genotype data."""

        payload = {"genotype_data": list(genotype_data)}
        response = self._client.post(
            f"/api/models/{model_id}/phenotype_prediction", json=payload
        )
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """Close the underlying HTTP client."""

        self._client.close()

    def __exit__(self, *exc_info) -> None:  # type: ignore[override]
        self.close()


def format_models_table(models: Iterable[dict]) -> str:
    """Create a human-readable table string for the model catalogue."""

    lines = ["Available Phenotype Models:"]
    for model in models:
        lines.append(f"- {model['display_name']} (id={model['id']}, version={model['version']})")
        description = model.get("description", "n/a")
        lines.append(f"  Description: {description}")
        supported_inputs = ", ".join(model.get("supported_inputs", []))
        lines.append(f"  Supported inputs: {supported_inputs or 'n/a'}")
        phenotypes = ", ".join(model.get("predictable_phenotypes", []))
        lines.append(f"  Predictable phenotypes: {phenotypes or 'n/a'}")
    return "\n".join(lines)


def load_genotype_values(csv_path: str | Path, column_name: str) -> List[str]:
    """Load genotype values from the specified CSV column."""

    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or column_name not in reader.fieldnames:
            raise KeyError(
                f"Column '{column_name}' not found in CSV. Available columns: {reader.fieldnames}"
            )

        values = [row.get(column_name, "") for row in reader]

    return values


if __name__ == "__main__":
    parser = ArgumentParser(description="Interact with the BRAI phenotype prediction API")
    parser.add_argument(
        "--model-id",
        help="When provided, fetch and display the phenotypes predicted by the given model",
    )
    parser.add_argument(
        "--predict-model-id",
        help="Request a phenotype prediction using genotype data for the specified model",
    )
    parser.add_argument(
        "--csv-path",
        default="csv/genotype_tomato.csv",
        help="Path to the genotype CSV file (default: csv/genotype_tomato.csv)",
    )
    parser.add_argument(
        "--csv-column",
        default="BP1150",
        help="Name of the CSV column containing genotype data (default: BP1150)",
    )
    args = parser.parse_args()

    with PhenotypeApiClient() as client:
        if args.predict_model_id:
            try:
                genotype_values = load_genotype_values(args.csv_path, args.csv_column)
            except (FileNotFoundError, KeyError) as error:
                print(f"Error loading genotype data: {error}")
            else:
                prediction = client.phenotype_prediction(
                    args.predict_model_id, genotype_values
                )
                print("Phenotype prediction response:")
                print(f"- Model ID: {prediction['model_id']}")
                print(f"- Genotype count: {prediction['genotype_count']}")
                print(f"- Prediction score: {prediction['prediction_score']:.6f}")
        elif args.model_id:
            phenotypes = client.list_model_phenotypes(args.model_id)
            if phenotypes:
                print(f"Phenotypes predicted by {args.model_id}:")
                for phenotype in phenotypes:
                    print(f"- {phenotype}")
            else:
                print(f"No phenotypes registered for model {args.model_id}.")
        else:
            models = client.list_models()
            print(format_models_table(models))
