"""Workspace model helpers."""

from __future__ import annotations

from typing import Any

from .client import get_client


def list_models() -> Any:
    """List all workspace models."""
    return get_client().list_models()


def get_model(id: str) -> Any:
    """Get a workspace model by id."""
    return get_client().get_model(id)


def create_model(
    id: str,
    name: str,
    base_model_id: str | None = None,
    description: str | None = None,
    system_prompt: str | None = None,
    params: dict[str, Any] | None = None,
    meta: dict[str, Any] | None = None,
    is_active: bool = True,
) -> Any:
    """Create a workspace model."""
    payload_meta = dict(meta or {})
    payload_params = dict(params or {})

    if description is not None:
        payload_meta["description"] = description
    if system_prompt is not None:
        payload_params.setdefault("system", system_prompt)

    payload = {
        "id": id,
        "name": name,
        "base_model_id": base_model_id,
        "meta": payload_meta,
        "params": payload_params,
        "is_active": is_active,
    }
    return get_client().create_model(payload)


def update_model(id: str, **kwargs: Any) -> Any:
    """Update a workspace model, merging provided fields onto the current model."""
    current = get_model(id)
    payload = {
        "id": id,
        "name": kwargs.pop("name", current.get("name", id)),
        "base_model_id": kwargs.pop("base_model_id", current.get("base_model_id")),
        "meta": dict(current.get("meta") or {}),
        "params": dict(current.get("params") or {}),
        "access_grants": kwargs.pop("access_grants", current.get("access_grants")),
        "is_active": kwargs.pop("is_active", current.get("is_active", True)),
    }

    if "description" in kwargs:
        payload["meta"]["description"] = kwargs.pop("description")
    if "system_prompt" in kwargs:
        payload["params"]["system"] = kwargs.pop("system_prompt")
    if "meta" in kwargs:
        payload["meta"].update(kwargs.pop("meta") or {})
    if "params" in kwargs:
        payload["params"].update(kwargs.pop("params") or {})

    payload.update(kwargs)
    return get_client().update_model(payload)


def delete_model(id: str) -> Any:
    """Delete a workspace model by id."""
    return get_client().delete_model(id)


def export_models() -> Any:
    """Export all workspace models."""
    return get_client().export_models()


def import_models(models_data: Any) -> Any:
    """Import workspace models."""
    return get_client().import_models(models_data)
