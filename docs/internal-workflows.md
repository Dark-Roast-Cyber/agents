# Internal Workflows

This document is for maintainers and AI coding tools working inside this repository. Keep public-facing project description in `README.md`; keep durable AI-agent guidance in `AGENTS.md` and this file.

## Operating Model

This repository is intentionally local-first and OpenCode-native.

1. Author locally.
2. Review locally.
3. Validate locally.
4. Publish outward only when needed.

OpenCode is the primary authoring environment. OpenWebUI is a publishing and runtime target. Local markdown remains the source of truth.

## OpenCode To OpenWebUI Mapping

| Local Artifact | OpenWebUI Artifact |
| --- | --- |
| Agent | Workspace Model |
| Skill | Skill |
| Command | Prompt |

## Sync Philosophy

- This repo is the source of truth for OpenCode-first authoring.
- OpenWebUI is a publish/import target, not the primary editing surface.
- Current sync is overwrite-oriented: push local markdown outward, or import tagged remote assets inward.
- Sync does not attempt bidirectional merge, conflict resolution, or delete propagation.
- Import remote models only when `meta.tags` contains a tag object with `name == "drc-agent"`.
- Ignore bulky UI-only fields during import/export, except preserve `meta.profile_image_url` when present so agent images survive sync.

## Naming Rules

- The filename slug is the canonical id.
- Display name defaults to the titleized filename slug.
- Example: `armis-query-agent.md` becomes `Armis Query Agent`.
- Prefer lowercase kebab-case filenames.
- Avoid duplicate concepts unless retaining a legacy compatibility entry intentionally.

## Local Authoring Workflow

- Edit durable agent behavior in `.opencode/agents/*.md`.
- Edit slash-style routing prompts in `.opencode/commands/*.md`.
- Edit reusable playbooks in `.opencode/skills/**/SKILL.md` or established skill markdown files.
- Treat local markdown as the source of truth for system prompts and prompt templates.
- Use the local `openwebui` Python package for sync, inspection, and API exploration.
- Push outward to OpenWebUI only after local review.
- Avoid hand-editing OpenWebUI when the change should live in repo source.

## Creating An Agent

1. Create a markdown file in `.opencode/agents/`.
2. Use the filename slug as the canonical id.
3. Add clear frontmatter, typically including `description`, `mode`, `temperature`, and `permission`.
4. Use `permission`, not the deprecated `tools` field.
5. Write concise, durable instructions that define identity, scope, and operating rules.
6. Update `AGENTS.md` and `README.md` inventories when the agent is public-facing.

Example frontmatter:

```yaml
---
description: Specialized assistant for a clear security workflow
mode: subagent
temperature: 0.1
permission:
  read: allow
  write: ask
  webfetch: ask
---
```

## Creating A Skill

1. Create a skill directory under `.opencode/skills/<skill-name>/` when using OpenCode skill format.
2. Add `.opencode/skills/<skill-name>/SKILL.md`.
3. Keep the skill reusable and identity-free.
4. Focus on workflow, policy, or repeatable instructions.
5. Name it clearly so its purpose is obvious from the slug.
6. Update inventories if the skill becomes part of the standard project workflow.

Example frontmatter:

```yaml
---
name: example-skill
description: Use when performing a specific repeatable workflow.
---
```

## Creating A Command

1. Create a markdown file in `.opencode/commands/`.
2. Set `agent: <agent-slug>` to define routing.
3. Set `subtask: false` unless there is a deliberate reason to isolate context.
4. Keep the body short and task-oriented.
5. Follow established error recovery and scope clarification patterns.
6. Update inventories when the command is added, renamed, or removed.

Example frontmatter:

```yaml
---
description: Short command description
agent: armis-query-agent
subtask: false
---
```

## Sync Tooling

Use `uv` from the repository root.

```bash
uv run --project openwebui python -m openwebui sync plan
uv run --project openwebui python -m openwebui sync push agents
uv run --project openwebui python -m openwebui sync push commands
uv run --project openwebui python -m openwebui sync push skills
uv run --project openwebui python -m openwebui sync push all
uv run --project openwebui python -m openwebui sync import agents
```

Practical rules:

- Run `sync plan` before push or import operations.
- Treat push operations as publish actions, not dry runs.
- Use `sync import agents` only for remote models intentionally tagged `drc-agent`.
- Keep runtime-specific sync behavior out of durable agent content unless it materially matters.

## Other OpenWebUI CLI Commands

```bash
uv run --project openwebui python -m openwebui models list
uv run --project openwebui python -m openwebui models get <id>
uv run --project openwebui python -m openwebui models create --id <id> --name <name> [--base-model ...] [--description ...] [--system-prompt ...]
uv run --project openwebui python -m openwebui models delete <id>
uv run --project openwebui python -m openwebui models export
uv run --project openwebui python -m openwebui tools list
uv run --project openwebui python -m openwebui functions list
uv run --project openwebui python -m openwebui prompts list
uv run --project openwebui python -m openwebui skills list
uv run --project openwebui python -m openwebui knowledge list
uv run --project openwebui python -m openwebui chat --model <model> --message <message>
```

## Avatar Workflow

- Store generated avatar source files in `.opencode/images/`.
- Prefer transparent PNG output for canonical avatar assets.
- Use JPEG only as a compatibility fallback for UI rendering tests.
- Preserve `meta.profile_image_url` during sync so pushed models do not lose assigned avatars.
- Let OpenWebUI handle framing; do not generate circles, badges, or background containers into the art.

Avatar prompt/style conventions live in `AI-AVATAR-PROMPT-STYLING-GUIDE.md`.

Generate images with `uv` from the repository root:

```bash
uv run --project openwebui python openwebui/generate_image.py \
  --prompt "<avatar prompt>" \
  --output "/absolute/path/to/output.png" \
  --background transparent \
  --format png
```

Environment variables:

- `OPENAI_API_KEY` is preferred.
- `OPEN_AI_API` is supported as a fallback for compatibility with prior local setup.

## Avatar Prompt Rules

- Follow `AI-AVATAR-PROMPT-STYLING-GUIDE.md`.
- Ask for polished chibi mascot styling, personality, and memorability.
- Infer likely gender presentation from the agent's identity when appropriate unless the user asks otherwise.
- Include the agent's unique primary color explicitly in the prompt.
- Prefer one subtle prop or clothing cue at most.
- Avoid floating UI, locks, digital particles, circles, badges, busy backgrounds, and generic cyber wallpaper.

## Validation

- Review markdown frontmatter before sync.
- Run a sync plan before any OpenWebUI push/import.
- Confirm inventories in `README.md` and `AGENTS.md` stay aligned with `.opencode/`.
- For behavior changes, check the relevant agent, command, or skill instructions directly rather than relying only on summaries.

## Armis Test Scenarios

1. Unprotected endpoint search: verify network device exclusion.
2. Critical vulnerability analysis: test risk prioritization.
3. Device lookup by hostname: validate multi-field search behavior.
4. Security software inventory: test vendor name variations.
5. Large result sets: verify file output formatting and summaries.

## Quality Checks

- Cross-check query results with alternate methods.
- Validate confidence scoring against query specificity.
- Test error recovery with ambiguous input.
- Verify file output format consistency.
- Confirm permission models still match intended usage.
