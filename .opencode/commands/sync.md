---
description: Sync agents, skills, and commands between this repo and OpenWebUI
agent: armis-query-agent
subtask: false
---

Run the OpenWebUI sync tooling to manage the relationship between this repo and the OpenWebUI server.

Available operations:
- `sync plan` — Read-only preview of what would be pushed or imported
- `sync push agents` — Push local agents to OpenWebUI workspace models
- `sync push commands` — Push local commands to OpenWebUI prompts
- `sync push skills` — Push local skills to OpenWebUI skills
- `sync push all` — Push all local resources to OpenWebUI
- `sync import agents` — Import tagged (drc-agent) models from OpenWebUI into local agent files

Run the appropriate sync command based on the user's request. Use the CLI:
  uv run --project openwebui python -m openwebui sync <operation>

Always run `sync plan` first if the user wants to push or import, so they can review what will change before it happens.
