"""Minimal OpenWebUI API client."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv

PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent
ENV_PATH = REPO_ROOT / ".env"
DEFAULT_TIMEOUT = 30.0


class OpenWebUIError(RuntimeError):
    """Raised when an OpenWebUI API request fails."""


class OpenWebUIClient:
    """Convenience client for the OpenWebUI REST API."""

    def __init__(
        self,
        api_key: str | None = None,
        api_spec_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        load_dotenv(ENV_PATH)
        self.api_key = api_key or os.getenv("OPEN_WEBUI_API_KEY")
        self.api_spec_url = api_spec_url or os.getenv("OPEN_WEBUI_API_SPEC")
        self.timeout = timeout

        if not self.api_key:
            raise OpenWebUIError(
                "Missing OPEN_WEBUI_API_KEY in environment or .env file."
            )
        if not self.api_spec_url:
            raise OpenWebUIError(
                "Missing OPEN_WEBUI_API_SPEC in environment or .env file."
            )

    @property
    def base_url(self) -> str:
        """Return the API base URL derived from the OpenAPI spec URL."""
        if self.api_spec_url.endswith("/openapi.json"):
            return self.api_spec_url[: -len("/openapi.json")]
        parsed = urlparse(self.api_spec_url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | list[Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> Any:
        """Send an authenticated request and return parsed JSON when available."""
        url = f"{self.base_url}{path}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.request(
                    method,
                    url,
                    params=params,
                    json=json_data,
                    files=files,
                    headers=headers,
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text.strip() or exc.response.reason_phrase
            raise OpenWebUIError(
                f"{method.upper()} {path} failed with {exc.response.status_code}: {detail}"
            ) from exc
        except httpx.HTTPError as exc:
            raise OpenWebUIError(f"{method.upper()} {path} failed: {exc}") from exc

        if response.status_code == 204 or not response.content:
            return {"ok": True}

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()
        return response.text

    def list_models(self) -> Any:
        """List all workspace models."""
        return self.request("GET", "/api/v1/models/list")

    def get_model(self, model_id: str) -> Any:
        """Get a workspace model by id."""
        return self.request("GET", "/api/v1/models/model", params={"id": model_id})

    def create_model(self, payload: dict[str, Any]) -> Any:
        """Create a workspace model."""
        return self.request("POST", "/api/v1/models/create", json_data=payload)

    def update_model(self, payload: dict[str, Any]) -> Any:
        """Update a workspace model."""
        return self.request("POST", "/api/v1/models/model/update", json_data=payload)

    def delete_model(self, model_id: str) -> Any:
        """Delete a workspace model."""
        return self.request(
            "POST", "/api/v1/models/model/delete", json_data={"id": model_id}
        )

    def export_models(self) -> Any:
        """Export workspace models."""
        return self.request("GET", "/api/v1/models/export")

    def import_models(self, payload: Any) -> Any:
        """Import workspace models."""
        return self.request("POST", "/api/v1/models/import", json_data=payload)

    def toggle_model(self, model_id: str) -> Any:
        """Toggle workspace model active state."""
        return self.request(
            "POST", "/api/v1/models/model/toggle", json_data={"id": model_id}
        )

    def update_model_access(self, payload: dict[str, Any]) -> Any:
        """Update workspace model access grants."""
        return self.request(
            "POST", "/api/v1/models/model/access/update", json_data=payload
        )

    def list_tools(self) -> Any:
        """List all tools."""
        return self.request("GET", "/api/v1/tools/list")

    def get_tool(self, tool_id: str) -> Any:
        """Get a tool by id."""
        return self.request("GET", f"/api/v1/tools/id/{tool_id}")

    def create_tool(self, payload: dict[str, Any]) -> Any:
        """Create a tool."""
        return self.request("POST", "/api/v1/tools/create", json_data=payload)

    def update_tool(self, tool_id: str, payload: dict[str, Any]) -> Any:
        """Update a tool."""
        return self.request(
            "POST", f"/api/v1/tools/id/{tool_id}/update", json_data=payload
        )

    def delete_tool(self, tool_id: str) -> Any:
        """Delete a tool."""
        return self.request("DELETE", f"/api/v1/tools/id/{tool_id}/delete")

    def list_functions(self) -> Any:
        """List all functions."""
        return self.request("GET", "/api/v1/functions/list")

    def get_function(self, function_id: str) -> Any:
        """Get a function by id."""
        return self.request("GET", f"/api/v1/functions/id/{function_id}")

    def create_function(self, payload: dict[str, Any]) -> Any:
        """Create a function."""
        return self.request("POST", "/api/v1/functions/create", json_data=payload)

    def update_function(self, function_id: str, payload: dict[str, Any]) -> Any:
        """Update a function."""
        return self.request(
            "POST", f"/api/v1/functions/id/{function_id}/update", json_data=payload
        )

    def delete_function(self, function_id: str) -> Any:
        """Delete a function."""
        return self.request("DELETE", f"/api/v1/functions/id/{function_id}/delete")

    def list_prompts(self) -> Any:
        """List all prompts."""
        return self.request("GET", "/api/v1/prompts/list")

    def get_prompt_by_command(self, command: str) -> Any:
        """Get a prompt by command."""
        return self.request("GET", f"/api/v1/prompts/command/{command}")

    def get_prompt(self, prompt_id: str) -> Any:
        """Get a prompt by id."""
        return self.request("GET", f"/api/v1/prompts/id/{prompt_id}")

    def create_prompt(self, payload: dict[str, Any]) -> Any:
        """Create a prompt."""
        return self.request("POST", "/api/v1/prompts/create", json_data=payload)

    def update_prompt(self, prompt_id: str, payload: dict[str, Any]) -> Any:
        """Update a prompt."""
        return self.request(
            "POST", f"/api/v1/prompts/id/{prompt_id}/update", json_data=payload
        )

    def delete_prompt(self, prompt_id: str) -> Any:
        """Delete a prompt."""
        return self.request("DELETE", f"/api/v1/prompts/id/{prompt_id}/delete")

    def list_skills(self) -> Any:
        """List all skills."""
        return self.request("GET", "/api/v1/skills/list")

    def get_skill(self, skill_id: str) -> Any:
        """Get a skill by id."""
        return self.request("GET", f"/api/v1/skills/id/{skill_id}")

    def create_skill(self, payload: dict[str, Any]) -> Any:
        """Create a skill."""
        return self.request("POST", "/api/v1/skills/create", json_data=payload)

    def update_skill(self, skill_id: str, payload: dict[str, Any]) -> Any:
        """Update a skill."""
        return self.request(
            "POST", f"/api/v1/skills/id/{skill_id}/update", json_data=payload
        )

    def delete_skill(self, skill_id: str) -> Any:
        """Delete a skill."""
        return self.request("DELETE", f"/api/v1/skills/id/{skill_id}/delete")

    def list_knowledge(self) -> Any:
        """List knowledge bases."""
        return self.request("GET", "/api/v1/knowledge/")

    def get_knowledge(self, knowledge_id: str) -> Any:
        """Get a knowledge base by id."""
        return self.request("GET", f"/api/v1/knowledge/{knowledge_id}")

    def create_knowledge(self, payload: dict[str, Any]) -> Any:
        """Create a knowledge base."""
        return self.request("POST", "/api/v1/knowledge/create", json_data=payload)

    def delete_knowledge(self, knowledge_id: str) -> Any:
        """Delete a knowledge base."""
        return self.request("DELETE", f"/api/v1/knowledge/{knowledge_id}/delete")

    def chat_completion(self, payload: dict[str, Any]) -> Any:
        """Send a chat completion request."""
        return self.request("POST", "/api/chat/completions", json_data=payload)

    def list_chats(self) -> Any:
        """List user chats."""
        return self.request("GET", "/api/v1/chats/list")

    def list_files(self) -> Any:
        """List files."""
        return self.request("GET", "/api/v1/files/")

    def upload_file(
        self, file_name: str, file_bytes: bytes, content_type: str | None = None
    ) -> Any:
        """Upload a file."""
        files = {
            "file": (file_name, file_bytes, content_type or "application/octet-stream")
        }
        return self.request("POST", "/api/v1/files/", files=files)


@lru_cache(maxsize=1)
def get_client() -> OpenWebUIClient:
    """Return a cached OpenWebUI client."""
    return OpenWebUIClient()
