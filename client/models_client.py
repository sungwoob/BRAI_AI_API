"""Simple client for interacting with the phenotype prediction API."""

from __future__ import annotations

from contextlib import AbstractContextManager
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
        lines.append(f"  Description: {model['description']}")
        supported_inputs = ", ".join(model.get("supported_inputs", []))
        lines.append(f"  Supported inputs: {supported_inputs or 'n/a'}")
    return "\n".join(lines)


if __name__ == "__main__":
    with PhenotypeApiClient() as client:
        models = client.list_models()
    print(format_models_table(models))
