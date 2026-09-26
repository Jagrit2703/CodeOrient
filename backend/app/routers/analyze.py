from fastapi import APIRouter, HTTPException

from app.schemas.analyze import AnalyzeRequest, ArchitectureMap
from app.services.architecture_agent import build_architecture_map
from app.services.repo_ingest import ingest_repo

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze", response_model=ArchitectureMap)
async def analyze(request: AnalyzeRequest) -> ArchitectureMap:
    try:
        context = ingest_repo(request.repo_url)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not ingest repo: {exc}") from exc
    if not context.modules:
        raise HTTPException(status_code=422, detail="No modules detected in this repo")
    return await build_architecture_map(context)
