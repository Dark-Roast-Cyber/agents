# Agents

OpenCode-first security operations assets for teams that need reusable agent behavior, slash-style commands, and shared playbooks.

This repository is designed to work across multiple harnesses and runtimes by keeping durable behavior in plain markdown and using lightweight sync tooling only when needed. It is intended for security operations, security services, and adjacent work such as Armis asset intelligence, vulnerability workflows, SOC triage, threat intelligence, code review, scripting, compliance, and vCISO guidance.

## What This Repo Is

- Local source of truth for agents, commands, and skills
- Markdown-first and portable across harnesses
- Built for OpenCode authoring and OpenWebUI publishing
- Focused on practical security operations and services workflows

## Compatibility Model

The content here is intentionally harness-agnostic:

- Durable behavior lives in `.opencode/agents/*.md`
- Reusable playbooks live in `.opencode/skills/*.md`
- Slash-style routing lives in `.opencode/commands/*.md`
- The `openwebui/` package provides sync and exploration tooling when you want to publish or inspect content

This keeps the repo usable in OpenCode while still being easy to adapt to other agent harnesses that consume markdown instructions.

## Repository Layout

```text
.opencode/
  agents/      # Durable agent personas and operating rules
  commands/    # Slash commands that route into agents
  skills/      # Reusable playbooks and workflow guidance
  images/      # Optional agent avatar assets
  package.json # OpenCode plugin dependency
openwebui/     # Local Python package for sync and API tooling
AGENTS.md      # Project guide and operating conventions
```

Trimmed `.opencode/` tree:

```text
.opencode/
  agents/
    ai-nyx-the-red-teamer.md
    armis-query-agent.md
    casey-the-compliance-analyst.md
    cisoinabox.md
    cody-the-code-security-analyst.md
    john-anderton-procog-analyst-clone.md
    logan-the-log-analyst.md
    madison-the-cybersecurity-manager.md
    soc-analyst.md
    sonny-the-soc-analyst.md
    stacey-the-scripter.md
    tim-the-threat-intel-analyst.md
  commands/
    search-armis.md
    search-device.md
    search-vulnerabilities.md
    sync.md
  skills/
    README.md
  images/
  package.json
```

## Included Capabilities

- Armis Standard Query workflows for devices, vulnerabilities, and activities
- SOC triage and incident support
- Threat intelligence research
- Secure code review and scripting assistance
- Compliance and governance guidance
- Cybersecurity management and vCISO support

## Local Workflow

This repo is designed to be cloned directly into a working directory and opened by OpenCode from that checkout.

In local development, the expected flow is:

1. `git clone` the repo
2. Open the cloned working directory in OpenCode
3. Edit the markdown assets in `.opencode/`
4. Review changes locally
5. Run a sync plan before publishing
6. Push to OpenWebUI only when you are ready

In production, the repo is used differently:

1. A container performs a `git pull` to refresh the repo state
2. OpenCode opens the working directory inside that container
3. The container sees the same markdown source of truth as the repo
4. Any publishing or sync step happens from that updated checkout

Common sync commands:

```bash
uv run --project openwebui python -m openwebui sync plan
uv run --project openwebui python -m openwebui sync push agents
uv run --project openwebui python -m openwebui sync push commands
uv run --project openwebui python -m openwebui sync push skills
uv run --project openwebui python -m openwebui sync push all
```

## Design Rules

- Keep prompts concise and operational
- Prefer platform-agnostic guidance unless harness behavior matters
- Use the smallest durable abstraction that fits the task
- Treat local markdown as authoritative
- Preserve security posture, validation, and confidence scoring where relevant

## Primary Use Cases

- Search and analysis support for Armis environments
- Repeatable security triage workflows
- Security operations and service delivery playbooks
- Reusable instructions for specialized analyst personas

## Notes

- `AGENTS.md` contains the detailed project guide and inventory
- The repo is structured for local authoring first, publishing second
- Avatar and image workflows are optional and handled locally when needed
