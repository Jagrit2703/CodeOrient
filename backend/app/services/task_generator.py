"""Scans the repo for TODO/FIXME/HACK signals and turns them into starter tasks."""

import asyncio
import re

from app.schemas.tasks import StarterTask, StarterTaskList
from app.services.ai_service import ai_service
from app.services.repo_ingest import RepoContext

SIGNAL_PATTERN = re.compile(r"(?:#|//|/\*|<!--)\s*(?:TODO|FIXME|HACK)\b[:\s]+(.+)")
MAX_TASKS = 8


def _scan_signals(context: RepoContext) -> list[tuple[str, str]]:
    signals: list[tuple[str, str]] = []
    for module in context.modules:
        for rel_path in module.files:
            full_path = context.local_path / rel_path
            try:
                text = full_path.read_text(errors="ignore")
            except OSError:
                continue
            for match in SIGNAL_PATTERN.finditer(text):
                signals.append((rel_path, match.group(1).strip()))
            if len(signals) >= MAX_TASKS * 2:
                break
        if len(signals) >= MAX_TASKS * 2:
            break
    return signals[:MAX_TASKS]


def _prompt(rel_path: str, note: str) -> str:
    return (
        "Turn this code comment into a short onboarding task for a new developer. "
        f"File: {rel_path}. Comment: {note}. "
        "Respond with one sentence describing the task."
    )


async def _build_task(rel_path: str, note: str) -> StarterTask:
    result = await asyncio.to_thread(ai_service.generate_task, _prompt(rel_path, note))
    return StarterTask(
        title=note[:60],
        description=result.output,
        difficulty="easy",
        target_files=[rel_path],
        why_this_teaches_the_system=f"Touches {rel_path}, a real file in this codebase.",
    )


async def build_starter_tasks(context: RepoContext) -> StarterTaskList:
    signals = _scan_signals(context)
    if not signals:
        return StarterTaskList(repo_url=context.repo_url, tasks=[])
    tasks = await asyncio.gather(*(_build_task(path, note) for path, note in signals))
    return StarterTaskList(repo_url=context.repo_url, tasks=list(tasks))
