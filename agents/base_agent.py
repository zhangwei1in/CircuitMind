"""Base agent class providing LLM client and common utilities.

Uses the OpenAI-compatible API so it works with DeepSeek, GPT, or any
provider that exposes a /chat/completions endpoint.
"""

from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI


class BaseAgent:
    """Thin wrapper around an OpenAI-compatible chat-completion client."""

    def __init__(
        self,
        name: str,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
    ):
        self.name = name
        self.model = model or os.getenv("CIRCUITAGENT_MODEL", "deepseek-chat")
        self.client = OpenAI(
            api_key=api_key or os.getenv("CIRCUITAGENT_API_KEY", "sk-placeholder"),
            base_url=base_url or os.getenv("CIRCUITAGENT_BASE_URL", "https://api.deepseek.com"),
        )

    def chat(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> str:
        """Send a single-turn chat and return the response text."""
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content or ""

    def chat_json(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.1,
    ) -> dict[str, Any]:
        """Chat and parse the response as JSON. Retries once on failure."""
        raw = self.chat(system_prompt, user_message, temperature)

        # Strip markdown code fences if present
        raw = raw.strip()
        if raw.startswith("```"):
            lines = raw.split("\n")
            # Remove opening fence
            lines = lines[1:]
            # Remove closing fence if present
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            raw = "\n".join(lines)

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Retry with a stricter prompt
            retry_msg = f"{user_message}\n\nReply with ONLY valid JSON, no markdown fences or extra text."
            raw2 = self.chat(system_prompt, retry_msg, temperature=0.0)
            raw2 = raw2.strip()
            if raw2.startswith("```"):
                lines = raw2.split("\n")
                lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                raw2 = "\n".join(lines)
            return json.loads(raw2)
