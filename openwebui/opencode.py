"""Helpers for reading and writing repo-local OpenCode markdown files."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent
OPENCODE_ROOT = REPO_ROOT / ".opencode"
AGENTS_DIR = OPENCODE_ROOT / "agents"
COMMANDS_DIR = OPENCODE_ROOT / "commands"
SKILLS_DIR = OPENCODE_ROOT / "skills"

FRONTMATTER_BOUNDARY = "---"
SLUG_WORD_RE = re.compile(r"[A-Za-z0-9]+")


@dataclass(slots=True)
class OpenCodeDocument:
    """Parsed OpenCode markdown document."""

    path: Path
    slug: str
    frontmatter: dict[str, Any]
    body: str

    @property
    def name(self) -> str:
        """Return the document display name."""
        value = self.frontmatter.get("name")
        return (
            value
            if isinstance(value, str) and value.strip()
            else titleize_slug(self.slug)
        )

    @property
    def description(self) -> str | None:
        """Return the document description."""
        value = self.frontmatter.get("description")
        if isinstance(value, str) and value.strip():
            return value.strip()
        return None


def titleize_slug(slug: str) -> str:
    """Convert a filename slug into a display title."""
    words = SLUG_WORD_RE.findall(slug.replace("_", "-"))
    return " ".join(word.capitalize() for word in words) or slug


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "None", "~"}:
        return None
    if value.startswith(('"', "'")) and value.endswith(('"', "'")) and len(value) >= 2:
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse simple YAML-like frontmatter and return metadata plus markdown body."""
    if not text.startswith(f"{FRONTMATTER_BOUNDARY}\n"):
        return {}, text

    lines = text.splitlines()
    try:
        end_index = lines[1:].index(FRONTMATTER_BOUNDARY) + 1
    except ValueError:
        return {}, text

    metadata: dict[str, Any] = {}
    active_map_key: str | None = None

    for line in lines[1:end_index]:
        if not line.strip():
            continue
        if line.startswith("  ") and active_map_key and ":" in line:
            key, raw_value = line.strip().split(":", 1)
            current = metadata.setdefault(active_map_key, {})
            if isinstance(current, dict):
                current[key.strip()] = _parse_scalar(raw_value)
            continue
        active_map_key = None
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not raw_value:
            metadata[key] = {}
            active_map_key = key
        else:
            metadata[key] = _parse_scalar(raw_value)

    body = "\n".join(lines[end_index + 1 :])
    if text.endswith("\n"):
        body += "\n"
    return metadata, body


def format_frontmatter(metadata: dict[str, Any]) -> str:
    """Serialize lightweight frontmatter."""
    lines = [FRONTMATTER_BOUNDARY]
    for key, value in metadata.items():
        if value is None:
            continue
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for nested_key, nested_value in value.items():
                lines.append(f"  {nested_key}: {_format_scalar(nested_value)}")
            continue
        lines.append(f"{key}: {_format_scalar(value)}")
    lines.append(FRONTMATTER_BOUNDARY)
    return "\n".join(lines)


def _format_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if not text or text.strip() != text or any(ch in text for ch in [":", "#"]):
        escaped = text.replace('"', '\\"')
        return f'"{escaped}"'
    return text


def load_markdown_document(path: Path) -> OpenCodeDocument:
    """Load a markdown document with optional frontmatter."""
    frontmatter, body = parse_frontmatter(path.read_text())
    return OpenCodeDocument(
        path=path,
        slug=path.stem,
        frontmatter=frontmatter,
        body=body,
    )


def list_documents(directory: Path) -> list[OpenCodeDocument]:
    """List markdown documents in a repo-local OpenCode directory."""
    if not directory.exists():
        return []
    return [load_markdown_document(path) for path in sorted(directory.glob("*.md"))]


def write_markdown_document(path: Path, frontmatter: dict[str, Any], body: str) -> None:
    """Write a markdown document with frontmatter."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        f"{format_frontmatter(frontmatter)}\n\n{body.rstrip()}\n"
        if body.strip()
        else f"{format_frontmatter(frontmatter)}\n"
    )
    path.write_text(text)
