"""Calls an AI model (Google Gemini by default, or Claude) and turns its reply into a list of hooks."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from . import prompts

PROVIDERS = {
    # name: default model
    "gemini": "gemini-flash-latest",  # free tier, no card needed
    "claude": "claude-sonnet-5-5",    # paid, needs Anthropic billing
}


@dataclass
class Hook:
    hook: str
    visual_text: str = ""
    tag: str = ""  # style for viral mode, angle for news mode


def parse_hooks(raw: str, tag_key: str) -> list[Hook]:
    """Pull the hooks out of the model's reply, even if it wrapped the JSON in extra text."""
    text = (raw or "").strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            raise ValueError("The AI reply did not contain any hooks. Please try again.")
        data = json.loads(match.group(0))

    items = data.get("hooks", []) if isinstance(data, dict) else data
    hooks = []
    for item in items:
        if isinstance(item, str):
            hooks.append(Hook(hook=item.strip()))
        elif isinstance(item, dict) and item.get("hook"):
            hooks.append(
                Hook(
                    hook=str(item["hook"]).strip(),
                    visual_text=str(item.get("visual_text", "")).strip(),
                    tag=str(item.get(tag_key, "")).strip(),
                )
            )
    if not hooks:
        raise ValueError("The AI reply did not contain any hooks. Please try again.")
    return hooks


class HookGenerator:
    def __init__(self, api_key: str, provider: str = "gemini", model: str = ""):
        if provider not in PROVIDERS:
            raise ValueError(f"Unknown provider '{provider}'. Use one of: {', '.join(PROVIDERS)}")
        self.provider = provider
        self.model = model or PROVIDERS[provider]
        self.api_key = api_key

    def _ask(self, system: str, user: str) -> str:
        if self.provider == "gemini":
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=user,
                config=types.GenerateContentConfig(
                    system_instruction=system,
                    response_mime_type="application/json",
                    temperature=1.0,
                ),
            )
            return response.text or ""

        from anthropic import Anthropic

        client = Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(block.text for block in response.content if block.type == "text")

    def viral_hooks(self, topic, platform, tone, language, count=8, audience="") -> list[Hook]:
        """Variation 1: topic -> viral hooklines + on-screen visual text."""
        user = prompts.viral_user_prompt(topic, platform, tone, language, count, audience)
        return parse_hooks(self._ask(prompts.VIRAL_SYSTEM, user), tag_key="style")

    def news_hooks(self, content, tone, language, count=6, platform="Facebook") -> list[Hook]:
        """Variation 2: news topic/content -> scroll-stopping news headlines."""
        user = prompts.news_user_prompt(content, tone, language, count, platform)
        return parse_hooks(self._ask(prompts.NEWS_SYSTEM, user), tag_key="angle")
