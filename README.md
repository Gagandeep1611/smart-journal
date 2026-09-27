# Personalized AI Journal

Personalized AI Journal is a full-stack journaling application with JWT authentication, per-user data isolation, vector-based retrieval, and an AI assistant that answers questions using only the authenticated user's journal entries.

The project is designed around a clear separation between the frontend, REST API, authentication, vector retrieval, and LLM provider layers.

## Features

- User registration and login
- JWT-based authentication
- Protected frontend routes
- Per-user journal entries
- Create, read, update, and delete journal entries
- Automatic embedding generation when journal entries are created or updated
- PostgreSQL + pgvector for vector storage and similarity search
- User-scoped vector retrieval
- RAG-based journal question answering
- Source citations for retrieved journal entries
- LLM provider abstraction
- Ollama ↔ OpenRouter provider switching through environment variables
- OpenAI embeddings
- React + TypeScript frontend
- Swagger/OpenAPI documentation
- Update/delete synchronization between journal data and embeddings

---

## Architecture

```text
┌─────────────────────────────┐
│      React Web Client       │
│     TypeScript + Vite       │
└──────────────┬──────────────┘
               │ REST / JSON
               ▼
┌─────────────────────────────┐
│       FastAPI Backend       │
│                             │
│ Auth │ Journal │ RAG │ API  │
└──────┬──────────────┬───────┘
       │              │
       │              ▼
       │      ┌─────────────────┐
       │      │   RAG Service   │
       │      └────────┬────────┘
       │               │
       │       ┌───────┴────────┐
       │       ▼                ▼
       │  Embeddings       LLM Provider
       │       │                │
       │       ▼           ┌────┴─────┐
       │   OpenAI         Ollama   OpenRouter
       │       │
       ▼       ▼
┌─────────────────────────────┐
│ PostgreSQL + pgvector       │
│                             │
│ Users                       │
│ Journal Entries             │
│ Journal Embeddings          │
└─────────────────────────────┘