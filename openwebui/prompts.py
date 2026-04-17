"""Prompt helpers."""

from __future__ import annotations

from typing import Any

from .client import get_client


def list_prompts() -> Any:
    """List all prompts."""
    return get_client().list_prompts()


def get_prompt(id: str) -> Any:
    """Get a prompt by id."""
    return get_client().get_prompt(id)


def create_prompt(command: str, name: str, content: str, **kwargs: Any) -> Any:
    """Create a prompt."""
    payload = {
        "command": command,
        "name": name,
        "content": content,
        "data": kwargs.pop("data", None),
        "meta": kwargs.pop("meta", None),
        "tags": kwargs.pop("tags", None),
        "access_grants": kwargs.pop("access_grants", None),
        "version_id": kwargs.pop("version_id", None),
        "commit_message": kwargs.pop("commit_message", None),
        "is_production": kwargs.pop("is_production", True),
    }
    payload.update(kwargs)
    return get_client().create_prompt(payload)


def update_prompt(id: str, **kwargs: Any) -> Any:
    """Update a prompt, merging provided fields onto the current prompt."""
    current = get_prompt(id)
    payload = {
        "command": kwargs.pop("command", current.get("command")),
        "name": kwargs.pop("name", current.get("name", id)),
        "content": kwargs.pop("content", current.get("content", "")),
        "data": kwargs.pop("data", current.get("data")),
        "meta": kwargs.pop("meta", current.get("meta")),
        "tags": kwargs.pop("tags", current.get("tags")),
        "access_grants": kwargs.pop("access_grants", current.get("access_grants")),
        "version_id": kwargs.pop("version_id", current.get("version_id")),
        "commit_message": kwargs.pop("commit_message", current.get("commit_message")),
        "is_production": kwargs.pop(
            "is_production", current.get("is_production", True)
        ),
    }
    payload.update(kwargs)
    return get_client().update_prompt(id, payload)


def delete_prompt(id: str) -> Any:
    """Delete a prompt by id."""
    return get_client().delete_prompt(id)
