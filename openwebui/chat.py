"""Chat helpers."""

from __future__ import annotations

from typing import Any

from .client import get_client


def chat_completion(model: str, messages: list[dict[str, Any]], **kwargs: Any) -> Any:
    """Send an OpenAI-compatible chat completion request."""
    payload = {"model": model, "messages": messages}
    payload.update(kwargs)
    return get_client().chat_completion(payload)


def list_chats() -> Any:
    """List the authenticated user's chats."""
    return get_client().list_chats()
