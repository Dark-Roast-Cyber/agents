"""Function helpers."""

from __future__ import annotations

from typing import Any

from .client import get_client


def list_functions() -> Any:
    """List all functions."""
    return get_client().list_functions()


def get_function(id: str) -> Any:
    """Get a function by id."""
    return get_client().get_function(id)


def create_function(
    id: str,
    name: str,
    content: str,
    description: str | None = None,
    manifest: dict[str, Any] | None = None,
) -> Any:
    """Create a function."""
    payload = {
        "id": id,
        "name": name,
        "content": content,
        "meta": {
            "description": description,
            "manifest": manifest,
        },
    }
    return get_client().create_function(payload)


def update_function(id: str, **kwargs: Any) -> Any:
    """Update a function, merging provided fields onto the current function."""
    current = get_function(id)
    payload = {
        "id": id,
        "name": kwargs.pop("name", current.get("name", id)),
        "content": kwargs.pop("content", current.get("content", "")),
        "meta": dict(current.get("meta") or {}),
    }
    if "description" in kwargs:
        payload["meta"]["description"] = kwargs.pop("description")
    if "manifest" in kwargs:
        payload["meta"]["manifest"] = kwargs.pop("manifest")
    if "meta" in kwargs:
        payload["meta"].update(kwargs.pop("meta") or {})
    payload.update(kwargs)
    return get_client().update_function(id, payload)


def delete_function(id: str) -> Any:
    """Delete a function by id."""
    return get_client().delete_function(id)
