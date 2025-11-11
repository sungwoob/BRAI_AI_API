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

To exercise the mocked phenotype prediction flow you can reuse the genotype
data stored in `csv/genotype_tomato.csv`. The client loads the `BP1150`
column, sends it to the server, and prints the returned prediction score:

```bash
python client/models_client.py --predict-model-id phenotype_classifier_v1
```

You can override the CSV location and column name via `--csv-path` and
`--csv-column` if you need to test alternative datasets.

## API Overview

- `GET /api/models` — returns the list of available phenotype prediction models.
- `GET /api/models/{model_id}/phenotypes` — returns the phenotypes the selected
  model can predict.
- `POST /api/models` — registers a new model in the mock catalogue using the
  payload schema shown below.
- `DELETE /api/models/{model_id}` — removes a model from the catalogue and
  returns the deleted entry.
- `POST /api/models/{model_id}/phenotype_prediction` — accepts genotype data
  and returns a mocked prediction score between 0 and 1.

Example payload for registering a model:

```json
{
  "id": "custom_model",
  "display_name": "Custom Model",
  "version": "0.1.0",
  "supported_inputs": ["example_input"],
  "predictable_phenotypes": ["example_phenotype"],
  "description": "Optional human readable summary"
}
```

The catalogue is currently populated with mock data until the model registry
service is connected. Prediction responses are also mocked and return a random
floating-point score in the `[0, 1]` range to emulate an inference call.

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
