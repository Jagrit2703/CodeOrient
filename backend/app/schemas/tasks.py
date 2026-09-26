from pydantic import BaseModel


class StarterTask(BaseModel):
    title: str
    description: str
    difficulty: str  # easy | medium | hard
    target_files: list[str]
    why_this_teaches_the_system: str


class StarterTaskList(BaseModel):
    repo_url: str
    tasks: list[StarterTask]
