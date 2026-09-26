# Personalized AI Journal

Personalized AI Journal is a FastAPI backend for account authentication and
private journal entry management. It provides JWT-based authentication,
user-owned journal storage, and Alembic database migrations.

## Current capabilities

- Register users with validated email addresses and password requirements.
- Hash passwords with `pwdlib` using its recommended password-hashing settings.
- Log in with email and password to receive a JWT bearer access token.
- Retrieve the authenticated user's profile.
- Create, list, read, update, and delete journal entries.
- Keep journal entries isolated to their owning user.
- Store creation timestamps for users and creation/update timestamps for entries.
- Expose health and root API endpoints.
- Manage the relational schema with Alembic.

> **Implementation status:** The API does not currently implement AI generation,
> summarization, or retrieval. LLM-related settings exist in configuration but
> are not used by any route.

## Technology stack

- Python 3.12+
- FastAPI
- SQLAlchemy
- PostgreSQL-compatible database via `psycopg`
- Alembic
- Pydantic Settings
- PyJWT
- `pwdlib[argon2]`
- Uvicorn
- `uv` for dependency and environment management

## Project structure

```text
smart-journal/
├── alembic/                    # Database migration environment and revisions
├── src/smart_journal/
│   ├── auth/                   # Authentication routes, JWT, and dependencies
│   ├── core/                   # Application settings
│   ├── db/                     # SQLAlchemy engine, session, and base model
│   ├── journal/                # Journal entry routes
│   ├── models/                 # User and journal-entry ORM models
│   ├── schemas/                # Request and response validation models
│   └── main.py                 # FastAPI application
├── alembic.ini                 # Alembic configuration
├── pyproject.toml              # Project metadata and dependencies
└── uv.lock                     # Locked dependency versions
```

## Prerequisites

- Python 3.12 or newer
- [`uv`](https://docs.astral.sh/uv/)
- PostgreSQL configured through `DATABASE_URL` (the documented setup uses the
  `psycopg` driver)

## Installation

From the project directory:

```bash
uv sync
```

Create a `.env` file in the project directory with the required database and
JWT settings. For example:

```bash
```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/smart_journal
JWT_SECRET=replace-this-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

`DATABASE_URL` is read by the database module, while `JWT_SECRET` is required by
the application settings. `JWT_ALGORITHM` defaults to `HS256` and
`ACCESS_TOKEN_EXPIRE_MINUTES` defaults to `30`. Optional settings include
`APP_NAME`, `APP_VERSION`, `DEBUG`, and the unused `LLM_PROVIDER`,
`LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL` values. Do not commit `.env` or
real secrets to source control.

## Database setup

Apply the existing migrations:

```bash
uv run alembic upgrade head
```

The migrations create:

- `users`: user identity, unique email, password hash, and creation timestamp.
- `journal_entries`: entry title/content, owner relationship, and timestamps.

To create a new migration after changing the models:

```bash
uv run alembic revision --autogenerate -m "describe the schema change"
uv run alembic upgrade head
```

## Running the API

Start the development server with:

```bash
uv run uvicorn smart_journal.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `GET /health`

## API endpoints

### Authentication

| Method | Endpoint | Authentication | Description |
| --- | --- | --- | --- |
| `POST` | `/auth/register` | No | Create a user account |
| `POST` | `/auth/login` | No | Return a JWT bearer token |
| `GET` | `/auth/me` | Bearer token | Return the current user |

Registration validates email addresses and requires passwords between 8 and
128 characters. It returns `409 Conflict` when the email is already in use.
Login returns `401 Unauthorized` for an unknown email or incorrect password.

### Journal entries

All journal endpoints require an `Authorization: Bearer <token>` header.

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/journal` | Create an entry |
| `GET` | `/journal` | List the current user's entries, newest first |
| `GET` | `/journal/{entry_id}` | Get one owned entry |
| `PUT` | `/journal/{entry_id}` | Update an owned entry |
| `DELETE` | `/journal/{entry_id}` | Delete an owned entry |

Journal titles are required and limited to 255 characters. Journal content must
contain at least one character. The update endpoint supports changing either
field independently; if neither field is supplied, the entry is still saved
and its `updated_at` timestamp is refreshed. Entries that do not exist or
belong to another user return `404 Not Found`.

## Example requests

Register:

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"reader@example.com","password":"correct-horse-battery-staple"}'
```

Log in and save the token:

```bash
TOKEN=$(
  curl -s -X POST http://127.0.0.1:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"reader@example.com","password":"correct-horse-battery-staple"}' |
  python -c 'import json, sys; print(json.load(sys.stdin)["access_token"])'
)
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

Run the application:

```bash
uv run uvicorn smart_journal.main:app --reload
```

Format and sort imports:

```bash
uv run black src
uv run isort src
```

The project currently does not include a test suite. The interactive OpenAPI
documentation at `/docs` can be used for manual endpoint verification.

## Security notes

- Keep `JWT_SECRET` private and use a long, randomly generated value outside
  development.
- Use HTTPS when exposing the API beyond localhost.
- Store production credentials in a secret manager or deployment environment,
  not in `.env` committed to the repository.
- JWT access tokens expire according to `ACCESS_TOKEN_EXPIRE_MINUTES` (30
  minutes by default).

## License

No license has been specified for this project yet.
