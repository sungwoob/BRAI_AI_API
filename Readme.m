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
`/api/models` endpoint.

## API Overview

- `GET /api/models` — returns the list of available phenotype prediction models.

The catalogue is currently populated with mock data until the model registry
service is connected.
