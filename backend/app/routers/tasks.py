from fastapi import APIRouter, HTTPException

from app.schemas.analyze import AnalyzeRequest
from app.schemas.tasks import StarterTaskList
from app.services.repo_ingest import ingest_repo
from app.services.task_generator import build_starter_tasks

router = APIRouter(prefix="/api", tags=["tasks"])


@router.post("/tasks", response_model=StarterTaskList)
async def tasks(request: AnalyzeRequest) -> StarterTaskList:
    try:
        context = ingest_repo(request.repo_url)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not ingest repo: {exc}") from exc
    return await build_starter_tasks(context)
