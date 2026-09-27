# Personalized AI Journal

A full-stack AI-powered journal application that allows users to securely store private journal entries and ask an AI assistant questions about their own journal history.

The application uses Retrieval-Augmented Generation (RAG) so that answers are grounded only in the authenticated user's journal entries.

## Features

- User registration and login
- JWT-based authentication
- Secure multi-user data isolation
- Create, read, update, and delete journal entries
- Automatic embedding generation when journal entries are created or updated
- Hosted PostgreSQL + pgvector for semantic search
- User-scoped vector retrieval
- RAG-powered journal chat
- LLM provider abstraction
- OpenRouter support
- Ollama support for local LLM inference
- OpenAI embeddings
- Source citations in chat responses
- Automatic synchronization of embeddings after journal updates and deletes
- Minimal React + TypeScript frontend
- FastAPI backend
- Environment-based configuration

## Architecture

```text
                         ┌──────────────────────┐
                         │   React Frontend     │
                         │ React + TypeScript   │
                         └──────────┬───────────┘
                                    │
                                    │ REST / JSON
                                    ▼
                         ┌──────────────────────┐
                         │   FastAPI Backend    │
                         │                      │
                         │ Authentication       │
                         │ Journal APIs         │
                         │ RAG APIs             │
                         └───────┬───────┬──────┘
                                 │       │
                    ┌────────────┘       └───────────────┐
                    ▼                                    ▼
          ┌───────────────────┐                 ┌───────────────────┐
          │ Supabase Postgres │                 │   LLM Abstraction │
          │ + pgvector        │                 │                   │
          │                   │                 │ OpenRouter        │
          │ Users             │                 │ Ollama            │
          │ Journal Entries   │                 └───────────────────┘
          │ Embeddings        │
          └───────────────────┘
                    ▲
                    │
                    │ Embeddings
                    │
          ┌───────────────────┐
          │ OpenAI Embeddings │
          │ text-embedding-   │
          │ 3-small           │
          └───────────────────┘
```

The backend is responsible for authentication, journal CRUD operations, embedding generation, vector retrieval, and RAG orchestration. PostgreSQL with pgvector stores journal data and embeddings, while retrieval is always scoped to the authenticated user's `user_id`.

The LLM layer is abstracted behind a common provider interface. The application can switch between OpenRouter and Ollama using environment variables without changing the RAG service or API layer.

## Tech Stack

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Pydantic Settings
- PyJWT
- OpenAI Python SDK
- pgvector

### Database

- Supabase PostgreSQL
- pgvector

### Frontend

- React
- TypeScript
- Vite
- Axios
- React Router

### AI

#### LLM Providers

- OpenRouter
- Ollama

#### Embeddings

- OpenAI `text-embedding-3-small`

## Project Structure

```text
smart-journal/
├── alembic/
│   └── versions/
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts
│   │   ├── components/
│   │   │   └── ProtectedRoute.tsx
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── Journal.tsx
│   │   │   └── Chat.tsx
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   └── package.json
│
├── src/
│   └── smart_journal/
│       ├── auth/
│       │   ├── dependencies.py
│       │   └── security.py
│       ├── core/
│       │   └── config.py
│       ├── db/
│       │   └── database.py
│       ├── embeddings/
│       │   ├── base.py
│       │   ├── factory.py
│       │   └── openai.py
│       ├── llm/
│       │   ├── base.py
│       │   ├── factory.py
│       │   ├── ollama.py
│       │   └── openrouter.py
│       ├── models/
│       ├── rag/
│       │   └── service.py
│       ├── routers/
│       │   ├── auth.py
│       │   └── journal.py
│       ├── schemas/
│       │   ├── auth.py
│       │   └── journal.py
│       └── services/
│           ├── embedding_service.py
│           └── vector_service.py
├── .env
├── .env.example
├── alembic.ini
├── pyproject.toml
├── uv.lock
└── README.md
```

## Prerequisites

- Python 3.12+
- `uv`
- Node.js and npm
- A Supabase project with PostgreSQL and pgvector enabled
- An OpenAI API key for embeddings
- An OpenRouter API key for the default LLM configuration
- Ollama is optional for local LLM inference

## 1. Clone the Repository

```bash
git clone git@github.com:Gagandeep1611/smart-journal.git
cd smart-journal
```

## 2. Install Backend Dependencies

This project uses `uv`.

```bash
uv sync
```

## 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add:

```env
APP_NAME=Personalized AI Journal
APP_VERSION=1.0.0
DEBUG=true

DATABASE_URL=<your-supabase-database-url>

JWT_SECRET=<your-jwt-secret>
JWT_ALGORITHM=HS256

# Active LLM: OpenRouter
LLM_PROVIDER=openrouter
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_API_KEY=<your-openrouter-api-key>
LLM_MODEL=openrouter/free

# Alternative LLM: Ollama
# LLM_PROVIDER=ollama
# LLM_BASE_URL=http://localhost:11434/v1
# LLM_API_KEY=ollama
# LLM_MODEL=llama3.2:1b

# Embeddings
EMBEDDING_PROVIDER=openai
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_API_KEY=<your-openai-api-key>
EMBEDDING_MODEL=text-embedding-3-small
```

Never commit `.env` or real API keys to Git.

## 4. Database Setup

The application uses Supabase PostgreSQL with pgvector.

```bash
uv run alembic upgrade head
```

The database contains users, journal entries, and journal embeddings.

The `journal_embeddings.embedding` column uses a 1536-dimensional vector generated using OpenAI `text-embedding-3-small`.

## 5. Run the Backend

```bash
uv run uvicorn smart_journal.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## 6. Run the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL shown by Vite, normally:

```text
http://localhost:5173
```

## Authentication

The application uses JWT-based authentication.

```text
Register
   │
   ▼
User stored in PostgreSQL
   │
   ▼
Login
   │
   ▼
JWT access token
   │
   ▼
Frontend stores token
   │
   ▼
Bearer token sent with protected requests
   │
   ▼
FastAPI validates token
   │
   ▼
Authenticated User object
```

Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

The authenticated user's ID is extracted from the JWT and used to scope database and vector operations.

## Multi-Tenancy and Data Isolation

Multi-tenancy is enforced at the backend service layer.

Every protected request is associated with an authenticated `user_id`. Journal queries are never performed using only a journal entry ID. Ownership is always part of the database query.

Conceptually:

```text
journal_entry.id = requested_id
AND
journal_entry.user_id = authenticated_user.id
```

The same ownership rule is applied to:

- Journal creation
- Journal listing
- Journal updates
- Journal deletion
- Vector retrieval
- RAG queries

This prevents one user from accessing another user's journal entries through manipulated IDs or search queries.

## Vector Database Isolation

Each journal embedding stores the corresponding `user_id`.

Vector retrieval applies user filtering before returning results.

```text
Semantic similarity search
        +
user_id filter
        +
journal ownership filter
        =
user-scoped retrieval
```

This prevents another user's journal entries from being included in the RAG context.

## LLM Provider Abstraction

The application defines a common `LLMProvider` interface:

```python
class LLMProvider(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
```

Currently supported providers:

- OpenRouter
- Ollama

The RAG service depends on the abstraction rather than directly depending on a specific provider.

Provider selection is controlled through:

```env
LLM_PROVIDER=openrouter
```

or:

```env
LLM_PROVIDER=ollama
```

### OpenRouter

```env
LLM_PROVIDER=openrouter
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_API_KEY=<your-openrouter-api-key>
LLM_MODEL=openrouter/free
```

### Ollama

```env
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=llama3.2:1b
```

OpenRouter provides a hosted LLM option, while Ollama provides local LLM inference.

## Embedding Provider

Embeddings are generated using OpenAI:

```env
EMBEDDING_PROVIDER=openai
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_API_KEY=<your-openai-api-key>
EMBEDDING_MODEL=text-embedding-3-small
```

OpenAI is used only for embeddings in the current architecture.

It is not an LLM provider in this project.

The embedding provider is isolated from the LLM provider so the two concerns can evolve independently.

## Journal Entry Lifecycle

When a user creates a journal entry:

```text
POST /journal
      │
      ▼
Validate request
      │
      ▼
Create journal entry
      │
      ▼
Generate embedding
      │
      ▼
Store embedding with user_id
      │
      ▼
Return journal entry
```

Each journal entry is currently treated as a single retrieval unit.

The MVP does not implement document chunking.

## Journal Updates

```text
PUT /journal/{entry_id}
      │
      ▼
Verify ownership
      │
      ▼
Update journal content
      │
      ▼
Generate new embedding
      │
      ▼
Update existing embedding
```

This keeps the vector representation synchronized with the latest journal content.

## Journal Deletes

```text
DELETE /journal/{entry_id}
      │
      ▼
Verify ownership
      │
      ▼
Delete associated embedding
      │
      ▼
Delete journal entry
```

This prevents deleted entries from remaining searchable.

## RAG Pipeline

```text
User Question
      │
      ▼
Generate Question Embedding
      │
      ▼
Vector Similarity Search
      │
      ▼
Filter by authenticated user_id
      │
      ▼
Retrieve relevant journal entries
      │
      ▼
Build context
      │
      ▼
Create grounded prompt
      │
      ▼
LLM Provider
      │
      ▼
Generate Answer
      │
      ▼
Return Answer + Sources
```

### 1. Query Embedding

The user's question is converted into a vector using the configured embedding provider.

### 2. Retrieval

The vector service performs cosine similarity search against stored journal embeddings.

Retrieval is scoped using the authenticated user's ID.

The current default retrieval configuration returns up to five relevant entries subject to the similarity threshold.

### 3. Context Construction

Retrieved entries are formatted into context containing:

- Journal title
- Journal content
- Similarity score

### 4. Generation

The RAG service sends a grounded prompt to the configured LLM provider.

The prompt instructs the model to:

- Use only the provided journal context
- Avoid inventing information
- Avoid unsupported assumptions
- State when the journal does not contain enough information

### 5. Sources

The response includes source metadata.

Example:

```json
{
  "answer": "You worked on your Spring Boot project.",
  "sources": [
    {
      "journal_entry_id": 11,
      "title": "Monday",
      "created_at": "2026-09-27T14:49:08.841197"
    }
  ]
}
```

The current implementation returns source metadata rather than complete source content.

## API Endpoints

### Authentication

#### Register

```http
POST /auth/register
```

#### Login

```http
POST /auth/login
```

### Journal

#### Create Journal Entry

```http
POST /journal
```

Creates a journal entry and generates its embedding.

#### List Journal Entries

```http
GET /journal
```

Returns journal entries belonging to the authenticated user.

#### Update Journal Entry

```http
PUT /journal/{entry_id}
```

Updates the journal entry and regenerates its embedding.

#### Delete Journal Entry

```http
DELETE /journal/{entry_id}
```

Deletes the journal entry and its associated embedding.

#### Chat With Journal

```http
POST /journal/chat
```

Runs the RAG pipeline against the authenticated user's journal entries.

## Example Chat Request

```json
{
  "question": "What did I work on in Java?"
}
```

## Frontend

The frontend is intentionally minimal and demonstrates the complete application flow.

### Login

Users can authenticate using their email and password.

### Register

New users can create an account.

### Journal

Authenticated users can:

- Create entries
- View entries
- Edit entries
- Delete entries

### Chat

Users can ask questions about their journal.

The response displays:

- AI-generated answer
- Source journal titles
- Source creation dates

## Environment Configuration

The repository contains a `.env.example` showing the required configuration.

The LLM can be switched without changing application code:

```env
LLM_PROVIDER=openrouter
```

or:

```env
LLM_PROVIDER=ollama
```

## Security Considerations

1. Never trust a `user_id` supplied by the frontend.
2. Always derive user identity from the authenticated JWT.
3. Scope journal queries using the authenticated user's ID.
4. Store `user_id` alongside vector embeddings.
5. Apply the `user_id` filter during vector similarity search.
6. Verify ownership before updating journal entries.
7. Verify ownership before deleting journal entries.
8. Never include another user's journal entries in RAG context.
9. Keep API keys and database credentials in environment variables.
10. Never commit `.env` to source control.

## RAG Failure Handling

If vector search does not find sufficiently relevant journal entries, the application does not send unrelated context to the LLM.

It returns:

```text
I couldn't find any relevant information in your journal to answer that question.
```

## Running With Ollama

Verify Ollama:

```bash
ollama list
```

Pull a model if necessary:

```bash
ollama pull llama3.2:1b
```

Configure:

```env
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=llama3.2:1b
```

Restart the backend after changing environment variables.

## Running With OpenRouter

Configure:

```env
LLM_PROVIDER=openrouter
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_API_KEY=<your-openrouter-api-key>
LLM_MODEL=openrouter/free
```

Restart the backend after changing environment variables.

## Development Commands

### Backend

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn smart_journal.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Demo Flow

```text
1. Open the frontend
2. Register a new user
3. Log in
4. Create a journal entry
5. Create another journal entry
6. Open the Chat page
7. Ask a question about the journal
8. Show the generated answer
9. Show returned source citations
10. Show backend terminal logs demonstrating the RAG flow
```

Example journal entry:

```text
Title:
Monday

Content:
Today I worked on a Spring Boot project. I implemented REST APIs,
worked with PostgreSQL, and fixed a problem in the authentication flow.
```

Example question:

```text
What did I work on in Java?
```

## Stretch Goals Implemented


- Update/delete synchronization between journal entries and embeddings
- Source citations in RAG responses

## Design Decisions

### Why FastAPI?

FastAPI provides:

- Type-safe request and response schemas
- Dependency injection
- Automatic OpenAPI documentation
- Straightforward REST API development
- Good support for AI/LLM integrations

### Why PostgreSQL + pgvector?

The application needs both relational application data and vector search.

PostgreSQL with pgvector provides:

- User and journal data in a relational database
- Vector embeddings in the same database
- SQL filtering by `user_id`
- Vector similarity search
- Strong ownership constraints

### Why OpenRouter and Ollama?

Both providers expose OpenAI-compatible interfaces, allowing the application to use a common abstraction.

OpenRouter provides a hosted LLM option, while Ollama provides a local LLM option.

### Why OpenAI for Embeddings?

The current implementation uses `text-embedding-3-small`, which produces 1536-dimensional embeddings and is supported by the configured pgvector column.

The embedding provider is isolated from the LLM provider so the two concerns can evolve independently.

## Limitations

- One journal entry is treated as one retrieval unit.
- No document chunking strategy is implemented.
- No streaming chat responses.
- Source citations currently return metadata only.
- The frontend is intentionally minimal.
- Embeddings currently use OpenAI.
- Only OpenRouter and Ollama are supported as LLM providers.

## Future Improvements

- Token-aware journal chunking
- Hybrid keyword + vector search
- Reranking retrieved results
- Streaming LLM responses
- Richer source citations
- Conversation history
- Journal tagging
- Date-aware retrieval
- Filtering by journal categories
- Background embedding jobs
- Retry and failure handling for external AI providers
- Automated integration tests
- Production deployment configuration
- Observability and structured RAG logging

## License

This project is intended as an engineering assignment/demo application.