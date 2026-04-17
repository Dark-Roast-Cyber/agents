"""Tool helpers."""

from __future__ import annotations

from typing import Any

from .client import get_client


def list_tools() -> Any:
    """List all tools."""
    return get_client().list_tools()


def get_tool(id: str) -> Any:
    """Get a tool by id."""
    return get_client().get_tool(id)


def create_tool(
    id: str,
    name: str,
    content: str,
    description: str | None = None,
    manifest: dict[str, Any] | None = None,
) -> Any:
    """Create a tool."""
    payload = {
        "id": id,
        "name": name,
        "content": content,
        "meta": {
            "description": description,
            "manifest": manifest or {},
        },
    }
    return get_client().create_tool(payload)


def update_tool(id: str, **kwargs: Any) -> Any:
    """Update a tool, merging provided fields onto the current tool."""
    current = get_tool(id)
    payload = {
        "id": id,
        "name": kwargs.pop("name", current.get("name", id)),
        "content": kwargs.pop("content", current.get("content", "")),
        "meta": dict(current.get("meta") or {}),
        "access_grants": kwargs.pop("access_grants", current.get("access_grants")),
    }
    if "description" in kwargs:
        payload["meta"]["description"] = kwargs.pop("description")
    if "manifest" in kwargs:
        payload["meta"]["manifest"] = kwargs.pop("manifest")
    if "meta" in kwargs:
        payload["meta"].update(kwargs.pop("meta") or {})
    payload.update(kwargs)
    return get_client().update_tool(id, payload)


def delete_tool(id: str) -> Any:
    """Delete a tool by id."""
    return get_client().delete_tool(id)
