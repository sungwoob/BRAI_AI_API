# BRAI AI API

This project exposes an HTTP interface for BRAI phenotype prediction models.

## Available scripts

To start the development server locally:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Querying the API from a client

After starting the server you can fetch the mocked model catalogue using the
bundled client script:

```bash
python client/models_client.py
```

The script prints a concise summary of the models returned by the
`/api/models` endpoint. To inspect the phenotypes available for a specific
model, pass its identifier via the `--model-id` option:

```bash
python client/models_client.py --model-id phenotype_classifier_v1
```

## API Overview

- `GET /api/models` — returns the list of available phenotype prediction models.
- `GET /api/models/{model_id}/phenotypes` — returns the phenotypes the selected
  model can predict.

The catalogue is currently populated with mock data until the model registry
service is connected.

### Managing mock AI models in code

For test scenarios you can extend or shrink the mocked catalogue using the
helpers in `app.services.model_catalog`:

```python
from app.services.model_catalog import register_model, unregister_model

register_model(
    required={
        "id": "custom_model",
        "display_name": "Custom Model",
        "version": "0.1.0",
        "supported_inputs": ["example_input"],
        "predictable_phenotypes": ["example_phenotype"],
    },
    optional={"description": "Demonstrates how to register a model."},
)

unregister_model("custom_model")
```

Required fields live under the `required` mapping, while metadata like the
description can be supplied via `optional`.
