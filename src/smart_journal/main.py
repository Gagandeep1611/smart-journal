from fastapi import FastAPI

app = FastAPI(
    title="Personalized AI Journal",
    description="AI-powered personal journal using RAG",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "Personalized AI Journal API"}


@app.get("/health")
async def health():
    return {"status": "ok"}