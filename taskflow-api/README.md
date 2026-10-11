# TaskFlow API

Async task management API with JWT authentication.

## Setup

```bash
cd taskflow-api
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
```

## Development

```bash
# Run server
uvicorn src.main:app --reload

# Run tests
pytest

# Format and lint
ruff check --fix
ruff format
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc