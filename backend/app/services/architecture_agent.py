"""Builds the Architecture & Impact Map by summarizing each detected module.

Runs one summarization call per module concurrently (asyncio.gather over
asyncio.to_thread) to mirror Bob 2.0's parallel subagent execution model.
"""

import asyncio

from app.schemas.analyze import ArchitectureMap, GraphEdge, GraphNode
from app.services.ai_service import ai_service
from app.services.repo_ingest import ModuleInfo, RepoContext


def _classify(module: ModuleInfo) -> str:
    name = module.name.lower()
    if any(k in name for k in ("frontend", "web", "ui", "client")):
        return "frontend"
    if any(k in name for k in ("db", "database", "migrations")):
        return "database"
    if any(k in name for k in ("backend", "api", "server")):
        return "backend"
    return "service"


def _prompt(module: ModuleInfo) -> str:
    file_list = "\n".join(module.files[:15])
    return (
        f"Summarize the purpose of the module '{module.name}' in one or two sentences, "
        f"based on these files:\n{file_list}"
    )


async def _summarize(module: ModuleInfo) -> GraphNode:
    result = await asyncio.to_thread(ai_service.summarize_module, _prompt(module))
    return GraphNode(
        id=module.name,
        label=module.name,
        type=_classify(module),
        summary=result.output,
        key_files=module.files[:8],
    )


def _detect_edges(modules: list[ModuleInfo]) -> list[GraphEdge]:
    edges = []
    for module in modules:
        for other in modules:
            if module.name == other.name:
                continue
            if any(other.name in f for f in module.files):
                edges.append(GraphEdge(source=module.name, target=other.name))
    return edges


async def build_architecture_map(context: RepoContext) -> ArchitectureMap:
    nodes = await asyncio.gather(*(_summarize(m) for m in context.modules))
    edges = _detect_edges(context.modules)
    return ArchitectureMap(repo_url=context.repo_url, nodes=list(nodes), edges=edges)
