from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from smart_journal.auth.router import router as auth_router
from smart_journal.journal.router import router as journal_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


app = FastAPI(
    title="Personalized AI Journal",
    description="AI-powered personal journal using RAG",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(journal_router)


@app.get("/")
async def root():
    return {"message": "Personalized AI Journal API"}


@app.get("/health")
async def health():
    return {"status": "ok"}
