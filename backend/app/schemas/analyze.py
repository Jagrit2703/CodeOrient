from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    repo_url: str


class GraphNode(BaseModel):
    id: str
    label: str
    type: str  # frontend | backend | database | external | service
    summary: str
    key_files: list[str]


class GraphEdge(BaseModel):
    source: str
    target: str
    type: str = "depends_on"


class ArchitectureMap(BaseModel):
    repo_url: str
    nodes: list[GraphNode]
    edges: list[GraphEdge]
