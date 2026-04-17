"""Skill helpers."""

from __future__ import annotations

from typing import Any

from .client import get_client


def list_skills() -> Any:
    """List all skills."""
    return get_client().list_skills()


def get_skill(id: str) -> Any:
    """Get a skill by id."""
    return get_client().get_skill(id)


def create_skill(
    id: str,
    name: str,
    content: str,
    description: str | None = None,
    meta: dict[str, Any] | None = None,
    is_active: bool = True,
    **kwargs: Any,
) -> Any:
    """Create a skill."""
    payload = {
        "id": id,
        "name": name,
        "description": description,
        "content": content,
        "meta": meta or {"tags": []},
        "is_active": is_active,
        "access_grants": kwargs.pop("access_grants", None),
    }
    payload.update(kwargs)
    return get_client().create_skill(payload)


def update_skill(id: str, **kwargs: Any) -> Any:
    """Update a skill, merging provided fields onto the current skill."""
    current = get_skill(id)
    payload = {
        "id": id,
        "name": kwargs.pop("name", current.get("name", id)),
        "description": kwargs.pop("description", current.get("description")),
        "content": kwargs.pop("content", current.get("content", "")),
        "meta": dict(current.get("meta") or {"tags": []}),
        "is_active": kwargs.pop("is_active", current.get("is_active", True)),
        "access_grants": kwargs.pop("access_grants", current.get("access_grants")),
    }
    if "meta" in kwargs:
        payload["meta"].update(kwargs.pop("meta") or {})
    payload.update(kwargs)
    return get_client().update_skill(id, payload)


def delete_skill(id: str) -> Any:
    """Delete a skill by id."""
    return get_client().delete_skill(id)
