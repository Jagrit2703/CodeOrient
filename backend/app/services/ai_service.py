"""Wraps IBM Watsonx / Granite calls for the Codebase Orientation pipeline.

Falls back to deterministic mock responses when no Watsonx credentials are
configured, so the architecture map and starter tasks work end-to-end
without a live IBM Cloud account.
"""

from dataclasses import dataclass

import httpx

from app.core.config import settings


@dataclass
class AIResult:
    output: str
    tokens_used: int
    model: str


class AIService:
    def __init__(self) -> None:
        self.enabled = bool(settings.watsonx_api_key and settings.watsonx_project_id)
        self._iam_token: str | None = None

    def _get_iam_token(self) -> str:
        if self._iam_token:
            return self._iam_token
        resp = httpx.post(
            "https://iam.cloud.ibm.com/identity/token",
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": settings.watsonx_api_key,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30,
        )
        resp.raise_for_status()
        self._iam_token = resp.json()["access_token"]
        return self._iam_token

    def _call_granite(self, prompt: str, max_new_tokens: int = 200) -> AIResult:
        token = self._get_iam_token()
        resp = httpx.post(
            f"{settings.watsonx_url}/ml/v1/text/generation?version=2023-05-29",
            json={
                "input": prompt,
                "model_id": settings.watsonx_model_id,
                "project_id": settings.watsonx_project_id,
                "parameters": {"max_new_tokens": max_new_tokens, "decoding_method": "greedy"},
            },
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        result = data["results"][0]
        return AIResult(
            output=result["generated_text"].strip(),
            tokens_used=result.get("generated_token_count", 0) + result.get("input_token_count", 0),
            model=settings.watsonx_model_id,
        )

    def _mock(self, prefix: str, prompt: str) -> AIResult:
        text = prompt.strip()
        return AIResult(
            output=f"[mock] {prefix}: {text[:160]}",
            tokens_used=max(1, len(text.split())),
            model="mock-granite",
        )

    def summarize_module(self, prompt: str) -> AIResult:
        if self.enabled:
            try:
                return self._call_granite(prompt)
            except Exception:
                # Demo-safe fallback: a Watsonx outage should never break the map.
                return self._mock("module summary", prompt)
        return self._mock("module summary", prompt)

    def generate_task(self, prompt: str) -> AIResult:
        if self.enabled:
            try:
                return self._call_granite(prompt)
            except Exception:
                return self._mock("starter task", prompt)
        return self._mock("starter task", prompt)


ai_service = AIService()
