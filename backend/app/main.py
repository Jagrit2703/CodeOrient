from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import analyze, tasks

app = FastAPI(
    title="Codebase Orientation API",
    description="Agentic developer onboarding: architecture maps and starter tasks for any repo, powered by IBM Granite & Watsonx.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)
app.include_router(tasks.router)


@app.get("/health")
def health():
    return {"status": "ok"}
