"""OpenCode/OpenWebUI sync workflows."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from .client import OpenWebUIClient, OpenWebUIError
from .opencode import (
    AGENTS_DIR,
    COMMANDS_DIR,
    SKILLS_DIR,
    list_documents,
    load_markdown_document,
    write_markdown_document,
)


DEFAULT_BASE_MODEL_ID = os.getenv(
    "OPEN_WEBUI_BASE_MODEL", "qwen3.6:35b-a3b-q4_K_M-ctx100k"
)


@dataclass(slots=True)
class ItemResult:
    """Result for one sync target."""

    kind: str
    slug: str
    action: str
    target: str
    path: str | None = None
    detail: str | None = None


def _items(response: Any) -> list[dict[str, Any]]:
    if isinstance(response, dict) and isinstance(response.get("items"), list):
        return [item for item in response["items"] if isinstance(item, dict)]
    if isinstance(response, list):
        return [item for item in response if isinstance(item, dict)]
    return []


def _index_by(items: Iterable[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        value = item.get(key)
        if isinstance(value, str) and value:
            result[value] = item
    return result


def _model_has_tag(model: dict[str, Any], tag_name: str) -> bool:
    tags = (model.get("meta") or {}).get("tags") or []
    for tag in tags:
        if isinstance(tag, dict) and tag.get("name") == tag_name:
            return True
    return False


def _is_not_found_error(exc: OpenWebUIError) -> bool:
    return " failed with 404:" in str(exc)


def _frontmatter_profile_image_url(frontmatter: dict[str, Any]) -> str | None:
    value = frontmatter.get("profile_image_url")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _model_profile_image_url(model: dict[str, Any] | None) -> str | None:
    if not isinstance(model, dict):
        return None
    value = (model.get("meta") or {}).get("profile_image_url")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _merge_agent_tags(existing_model: dict[str, Any] | None) -> list[dict[str, Any]]:
    tags = []
    seen_names: set[str] = set()

    if isinstance(existing_model, dict):
        existing_tags = (existing_model.get("meta") or {}).get("tags") or []
        if isinstance(existing_tags, list):
            for tag in existing_tags:
                if not isinstance(tag, dict):
                    continue
                name = tag.get("name")
                if not isinstance(name, str):
                    continue
                normalized_name = name.strip()
                if not normalized_name or normalized_name in seen_names:
                    continue
                tags.append({**tag, "name": normalized_name})
                seen_names.add(normalized_name)

    if "drc-agent" not in seen_names:
        tags.append({"name": "drc-agent"})

    return tags


def _build_agent_payload(
    doc: Any, existing_model: dict[str, Any] | None = None
) -> dict[str, Any]:
    meta: dict[str, Any] = {
        "description": doc.description,
        "tags": _merge_agent_tags(existing_model),
    }
    profile_image_url = _frontmatter_profile_image_url(doc.frontmatter)
    if profile_image_url is None:
        profile_image_url = _model_profile_image_url(existing_model)
    if profile_image_url is not None:
        meta["profile_image_url"] = profile_image_url

    return {
        "id": doc.slug,
        "name": doc.name,
        "base_model_id": DEFAULT_BASE_MODEL_ID,
        "meta": meta,
        "params": {"system": doc.body.rstrip()},
        "is_active": True,
    }


def plan_sync(client: OpenWebUIClient) -> dict[str, Any]:
    """Build a read-only sync plan summary."""
    local_agents = list_documents(AGENTS_DIR)
    local_commands = list_documents(COMMANDS_DIR)
    local_skills = [
        doc for doc in list_documents(SKILLS_DIR) if doc.slug.lower() != "readme"
    ]

    remote_models = _items(client.list_models())
    remote_prompts = _items(client.list_prompts())
    remote_skills = _items(client.list_skills())

    model_index = _index_by(remote_models, "id")
    prompt_index = _index_by(remote_prompts, "command")
    skill_index = _index_by(remote_skills, "id")
    tagged_models = [
        model for model in remote_models if _model_has_tag(model, "drc-agent")
    ]

    return {
        "agents": {
            "local": len(local_agents),
            "remote_existing": sum(
                1 for doc in local_agents if doc.slug in model_index
            ),
            "remote_missing": sorted(
                doc.slug for doc in local_agents if doc.slug not in model_index
            ),
        },
        "commands": {
            "local": len(local_commands),
            "remote_existing": sum(
                1 for doc in local_commands if doc.slug in prompt_index
            ),
            "remote_missing": sorted(
                doc.slug for doc in local_commands if doc.slug not in prompt_index
            ),
        },
        "skills": {
            "local": len(local_skills),
            "remote_existing": sum(
                1 for doc in local_skills if doc.slug in skill_index
            ),
            "remote_missing": sorted(
                doc.slug for doc in local_skills if doc.slug not in skill_index
            ),
            "api_supported": True,
        },
        "import_agents": {
            "remote_tagged": len(tagged_models),
            "repo_paths": sorted(
                f".opencode/agents/{model['id']}.md"
                for model in tagged_models
                if model.get("id")
            ),
        },
    }


def push_agents(client: OpenWebUIClient) -> dict[str, Any]:
    """Publish local agents to OpenWebUI models."""
    documents = list_documents(AGENTS_DIR)
    results: list[ItemResult] = []

    for doc in documents:
        try:
            existing_model = client.get_model(doc.slug)
        except OpenWebUIError as exc:
            if not _is_not_found_error(exc):
                raise
            existing_model = None
            payload = _build_agent_payload(doc)
            client.create_model(payload)
            action = "created"
        else:
            payload = _build_agent_payload(doc, existing_model)
            client.update_model(payload)
            action = "updated"
        results.append(ItemResult("agent", doc.slug, action, f"model:{doc.slug}"))

    return _summary("push_agents", results)


def push_commands(client: OpenWebUIClient) -> dict[str, Any]:
    """Publish local commands to OpenWebUI prompts."""
    documents = list_documents(COMMANDS_DIR)
    results: list[ItemResult] = []

    for doc in documents:
        payload = {
            "command": doc.slug,
            "name": doc.name,
            "content": doc.body.rstrip(),
        }
        try:
            existing = client.get_prompt_by_command(doc.slug)
        except OpenWebUIError as exc:
            if not _is_not_found_error(exc):
                raise
            client.create_prompt(payload)
            action = "created"
            target = f"prompt:{doc.slug}"
        else:
            client.update_prompt(str(existing["id"]), payload)
            action = "updated"
            target = f"prompt:{existing['id']}"
        results.append(ItemResult("command", doc.slug, action, target))

    return _summary("push_commands", results)


def push_skills(client: OpenWebUIClient) -> dict[str, Any]:
    """Publish local skills to OpenWebUI skills."""
    documents = [
        doc for doc in list_documents(SKILLS_DIR) if doc.slug.lower() != "readme"
    ]
    results: list[ItemResult] = []

    for doc in documents:
        payload = {
            "id": doc.slug,
            "name": doc.name,
            "description": doc.description,
            "content": doc.body.rstrip(),
            "meta": {"tags": []},
            "is_active": True,
        }
        try:
            client.get_skill(doc.slug)
        except OpenWebUIError as exc:
            if not _is_not_found_error(exc):
                raise
            client.create_skill(payload)
            action = "created"
        else:
            client.update_skill(doc.slug, payload)
            action = "updated"
        results.append(ItemResult("skill", doc.slug, action, f"skill:{doc.slug}"))

    return _summary("push_skills", results)


def import_agents(client: OpenWebUIClient) -> dict[str, Any]:
    """Import tagged OpenWebUI models into repo-local agent markdown files."""
    results: list[ItemResult] = []
    for model in _items(client.list_models()):
        if not _model_has_tag(model, "drc-agent"):
            continue
        model_id = model.get("id")
        if not isinstance(model_id, str) or not model_id:
            continue
        path = AGENTS_DIR / f"{model_id}.md"
        existed_before = path.exists()
        existing_frontmatter: dict[str, Any] = {}
        if existed_before:
            existing_frontmatter = load_markdown_document(path).frontmatter
        frontmatter = dict(existing_frontmatter)
        description = (model.get("meta") or {}).get("description")
        if isinstance(description, str) and description.strip():
            frontmatter["description"] = description.strip()
        profile_image_url = _model_profile_image_url(model)
        if profile_image_url is not None:
            frontmatter["profile_image_url"] = profile_image_url
        frontmatter.setdefault("mode", "primary")
        body = ((model.get("params") or {}).get("system") or "").rstrip()
        write_markdown_document(path, frontmatter, body)
        results.append(
            ItemResult(
                "agent",
                model_id,
                "updated" if existed_before else "created",
                f"file:{path.name}",
                path=str(path),
            )
        )

    return _summary("import_agents", results)


def _summary(operation: str, results: list[ItemResult]) -> dict[str, Any]:
    return {
        "operation": operation,
        "count": len(results),
        "items": [asdict(result) for result in results],
    }
