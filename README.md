# Personalized AI Journal

Personalized AI Journal is a FastAPI app for private journaling with JWT authentication, user-owned journal entries, and a vector-search/RAG layer for semantic recall over a user's journal history.

## Overview

The application includes:

- User registration and login
- JWT bearer authentication
- Per-user journal CRUD APIs
- SQLAlchemy + PostgreSQL persistence
- pgvector-based similarity search for journal entries
- OpenAI-compatible LLM and embedding providers
- Alembic database migrations

The implementation lives in `src/smart_journal` and is organized by concern: auth, journal, models, services, embeddings, LLM providers, and RAG.

## Current implementation status

The code currently supports these live features:

- Register users with email validation and password requirements
- Hash passwords using `pwdlib[argon2]`
- Log in and receive a JWT access token
- Fetch the authenticated user profile via `/auth/me`
- Create, list, get, update, and delete journal entries
- Restrict entries to the authenticated user
- Generate embedding vectors for each journal entry
- Search for similar journal entries by user and cosine distance
- Answer user questions using the retrieved journal context through `RAGService`

The RAG pipeline exists as a service layer, but it is not exposed through a dedicated FastAPI route in the current app.

## Technology stack

- Python 3.12+
- FastAPI
- SQLAlchemy
- PostgreSQL + `psycopg`
- pgvector
- Alembic
- Pydantic Settings
- PyJWT
- `pwdlib[argon2]`
- OpenAI Python client
- Uvicorn
- `uv` for dependency management

## Project structure

```text
smart-journal/
├── alembic/                          # Alembic migrations and environment
│   └── versions/
├── src/smart_journal/
│   ├── auth/                        # Auth routes, dependencies, JWT helpers
│   ├── core/                        # Settings and environment config
│   ├── db/                          # Engine/session setup
│   ├── embeddings/                  # Embedding provider implementations
│   ├── journal/                     # Journal routes
│   ├── llm/                         # LLM provider implementations
│   ├── models/                      # SQLAlchemy ORM models
│   ├── rag/                         # RAG orchestration service
│   ├── schemas/                     # Pydantic schemas
│   ├── services/                    # Embedding/vector helpers
│   ├── tests/                       # Local test module
│   ├── main.py                      # FastAPI application entrypoint
│   └── __init__.py
├── alembic.ini
├── pyproject.toml
├── README.md
├── test_llm.py                     # Manual LLM smoke test
├── test_rag.py                     # Manual RAG smoke test
├── test_vector_search.py           # Manual vector-search smoke test
├── uv.lock
└── .env (created locally, not committed)
```

## Requirements

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/)
- PostgreSQL with a configured `DATABASE_URL`
- pgvector-enabled Postgres for the `journal_embeddings` table

## Installation

From the project directory:

```bash
uv sync
```

Create a `.env` file in the project root with the required settings. Example:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/smart_journal
JWT_SECRET=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=
LLM_MODEL=llama3.1

EMBEDDING_PROVIDER=ollama
EMBEDDING_BASE_URL=http://localhost:11434/v1
EMBEDDING_API_KEY=
EMBEDDING_MODEL=nomic-embed-text
```

Notes:

- `DATABASE_URL` is required by the DB setup
- `JWT_SECRET` is required by the settings model
- `JWT_ALGORITHM` defaults to `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` defaults to `30`
- `LLM_*` and `EMBEDDING_*` values are used by the provider factories
- Do not commit `.env` or real secrets to source control

## Database setup

Create or update the schema with Alembic:

```bash
uv run alembic upgrade head
```

The migrations currently manage:

- `users`: email, password hash, and created timestamp
- `journal_entries`: title, content, ownership, and timestamps
- `journal_embeddings`: embedding vectors and metadata per journal entry

To add a new migration after model changes:

```bash
uv run alembic revision --autogenerate -m "describe the change"
uv run alembic upgrade head
```

## Running the app

Start the development server:

```bash
uv run uvicorn smart_journal.main:app --reload
```

The app is available at:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `GET /health`

## API endpoints

### Authentication

| Method | Endpoint | Auth required | Description |
| --- | --- | --- | --- |
| `POST` | `/auth/register` | No | Create a new user |
| `POST` | `/auth/login` | No | Authenticate and receive a JWT |
| `GET` | `/auth/me` | Yes | Return the authenticated user |

Behavior:

- Registration validates the email format.
- Password length must be 8 to 128 characters.
- Duplicate email addresses return `409 Conflict`.
- Bad credentials return `401 Unauthorized`.

### Journal entries

All journal routes require a bearer token in the `Authorization` header.

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/journal` | Create a journal entry |
| `GET` | `/journal` | List the current user's entries, newest first |
| `GET` | `/journal/{entry_id}` | Fetch one journal entry |
| `PUT` | `/journal/{entry_id}` | Update one journal entry |
| `DELETE` | `/journal/{entry_id}` | Delete one journal entry |

Validation:

- Journal title is required and capped at 255 characters.
- Journal content is required and must be at least 1 character.
- Update requests can change title, content, or both.
- `updated_at` is refreshed on updates.
- Missing or foreign journal entries return `404 Not Found`.

## Vector search and RAG

The app includes a vector retrieval pipeline for journal entries:

1. A journal entry is embedded when created.
2. The query text is embedded with the configured embedding provider.
3. `search_similar_entries()` retrieves user-specific matches using pgvector cosine distance.
4. `RAGService.answer_question()` builds a prompt from relevant entries and queries the configured LLM.

Relevant files:

- `src/smart_journal/services/embedding_service.py`
- `src/smart_journal/services/vector_service.py`
- `src/smart_journal/rag/service.py`
- `src/smart_journal/models/journal_embedding.py`

This pipeline is implemented as a service layer and not currently routed through a dedicated endpoint.

## Example requests

Register:

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"reader@example.com","password":"correct-horse-battery-staple"}'
```

Log in and capture the token:

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"reader@example.com","password":"correct-horse-battery-staple"}' \
  | python -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')
```

Create a journal entry:

```bash
curl -X POST http://127.0.0.1:8000/journal \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"A good day","content":"I made time to write today."}'
```

List entries:

```bash
curl http://127.0.0.1:8000/journal \
  -H "Authorization: Bearer $TOKEN"
```

## Development commands

Run the app:

```bash
uv run uvicorn smart_journal.main:app --reload
```

Format code:

```bash
uv run black src
uv run isort src
```

Manual smoke tests for the LLM and retrieval pieces can be run with:

```bash
python test_llm.py
python test_rag.py
python test_vector_search.py
```

## Security notes

- Keep `JWT_SECRET` private and generate it outside the repository in production.
- Use HTTPS whenever the app is exposed beyond localhost.
- Store database credentials and API keys in environment or secret-manager systems, not in committed files.
- JWT tokens expire according to `ACCESS_TOKEN_EXPIRE_MINUTES`.

## License

No license has been specified for this project yet.
