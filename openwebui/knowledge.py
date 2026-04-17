"""Knowledge base helpers."""

from __future__ import annotations

from typing import Any

from .client import get_client


def list_knowledge() -> Any:
    """List all knowledge bases."""
    return get_client().list_knowledge()


def get_knowledge(id: str) -> Any:
    """Get a knowledge base by id."""
    return get_client().get_knowledge(id)


def create_knowledge(name: str, description: str | None = None) -> Any:
    """Create a knowledge base."""
    payload = {"name": name, "description": description}
    return get_client().create_knowledge(payload)


def delete_knowledge(id: str) -> Any:
    """Delete a knowledge base by id."""
    return get_client().delete_knowledge(id)
