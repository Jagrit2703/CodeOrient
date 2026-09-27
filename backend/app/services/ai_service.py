"""Wraps IBM Bob's hosted inference API for the Codebase Orientation pipeline.

Falls back to deterministic mock responses when no Bob API key is configured,
so the architecture map and starter tasks work end-to-end without one.
"""

import logging
from dataclasses import dataclass

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class AIResult:
    output: str
    tokens_used: int
    model: str


class AIService:
    def __init__(self) -> None:
        self.enabled = bool(settings.ibm_bob_api_key)

    def _call_bob(self, prompt: str, max_tokens: int = 200) -> AIResult:
        resp = httpx.post(
            f"{settings.ibm_bob_base_url}/chat/completions",
            json={
                "model": settings.ibm_bob_model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
            },
            headers={
                "Authorization": f"Bearer {settings.ibm_bob_api_key}",
                "Content-Type": "application/json",
            },
            timeout=60,
        )
        if resp.is_error:
            logger.error(
                "IBM Bob returned HTTP %s: %s",
                resp.status_code,
                resp.text[:500],
            )
        resp.raise_for_status()
        data = resp.json()
        choice = data["choices"][0]
        usage = data.get("usage", {})
        return AIResult(
            output=choice["message"]["content"].strip(),
            tokens_used=usage.get("total_tokens", 0),
            model=settings.ibm_bob_model,
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
                return self._call_bob(prompt)
            except Exception:
                # Demo-safe fallback: a gateway outage should never break the map.
                logger.exception("IBM Bob call failed for module summary; falling back to mock")
                return self._mock("module summary", prompt)
        return self._mock("module summary", prompt)

    def generate_task(self, prompt: str) -> AIResult:
        if self.enabled:
            try:
                return self._call_bob(prompt)
            except Exception:
                logger.exception("IBM Bob call failed for starter task; falling back to mock")
                return self._mock("starter task", prompt)
        return self._mock("starter task", prompt)


ai_service = AIService()
