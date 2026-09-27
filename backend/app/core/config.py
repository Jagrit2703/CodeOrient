from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolved relative to this file (not the process's CWD) so `.env` at the
# project root is found whether uvicorn is launched from `backend/` or from
# the repo root. Under Docker this path doesn't exist inside the container,
# which is fine — docker-compose's `env_file:` already injects real env vars.
_PROJECT_ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_PROJECT_ROOT_ENV, extra="ignore")

    ibm_bob_api_key: str = ""
    ibm_bob_base_url: str = "https://api.us-east.bob.ibm.com/inference/v1"
    ibm_bob_model: str = "ibm/granite-3-8b-instruct"

    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
