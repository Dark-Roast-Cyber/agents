# Security Agents Project Guide

This repository manages OpenCode-first security operations assets: agents, skills, and slash commands authored as local markdown. The public README should describe what the project offers to humans. Internal operating guidance for AI coding tools belongs here or in linked internal docs.

## Source Of Truth

- Local markdown files are authoritative.
- OpenWebUI is a publish/import target, not the primary editing surface.
- Agents live in `.opencode/agents/`.
- Commands live in `.opencode/commands/`.
- Skills live in `.opencode/skills/`.
- Optional avatar assets live in `.opencode/images/`.
- Sync and API tooling lives in `openwebui/`.

## Internal Workflow Docs

Use `docs/internal-workflows.md` for detailed local authoring, agent creation, skill creation, command creation, avatar generation, and OpenWebUI sync/deployment workflows.

Keep `README.md` public-facing and avoid placing internal runtime, sync, or AI-coding instructions there.

## Project Layout

```text
/
├── .opencode/
│   ├── agents/
│   ├── commands/
│   ├── skills/
│   ├── images/
│   └── package.json
├── docs/
│   └── internal-workflows.md
├── openwebui/
├── AGENTS.md
├── README.md
├── AGENTIC-SYSTEM-PROMPT-STYLE-GUIDE.md
└── AI-AVATAR-PROMPT-STYLING-GUIDE.md
```

## Editing Rules

- Preserve the markdown-first model.
- Use the smallest durable abstraction that matches the task.
- Edit agent behavior in `.opencode/agents/*.md`.
- Edit slash-style routing prompts in `.opencode/commands/*.md`.
- Edit reusable playbooks in `.opencode/skills/**/SKILL.md` or established skill markdown files.
- Keep prompt guidance platform-agnostic unless the detail is specifically about this repo's sync/runtime behavior.
- Update inventories when adding, renaming, or removing agents, commands, or durable skills.
- Use `permission`, not the deprecated `tools` field, in OpenCode agent frontmatter.
- Prefer lowercase kebab-case filenames and treat the filename slug as canonical.

## When To Create Artifacts

### Agent

Create an agent when the change defines a durable persona or long-lived behavior that a user would plausibly select as a model or delegate to as a specialist.

### Skill

Create a skill when the change is a reusable workflow, playbook, policy, or repeatable instruction set. Skills should be guidance, not identity.

### Command

Create a command when the change is a slash-style shortcut or routing prompt for a common task.

## Agent Inventory

| File | Purpose | Mode | Description |
| --- | --- | --- | --- |
| `.opencode/agents/armis-query-agent.md` | Armis ASQ query agent | all | Translates natural-language security requests into validated Armis Standard Query workflows. |
| `.opencode/agents/splunk-assistant.md` | Splunk operations | all | Handles Splunk search, discovery, alerting, saved searches, and operational workflows using Splunk MCP tools. |
| `.opencode/agents/soc-analyst.md` | SOC analysis | subagent | Supports SOC investigations and security analysis tasks. |
| `.opencode/agents/sonny-the-soc-analyst.md` | SOC triage | subagent | Provides verdict-oriented alert triage and next-step guidance for investigations. |
| `.opencode/agents/tim-the-threat-intel-analyst.md` | Threat intelligence analysis | subagent | Performs CTI analysis on threat reports, indicators, campaigns, and threat actors. |
| `.opencode/agents/john-anderton-procog-analyst-clone.md` | CTI/IOC research | subagent | Summarizes IOCs, actors, campaigns, and TTPs for concise CTI workflows. |
| `.opencode/agents/ai-nyx-the-red-teamer.md` | Red team/vuln assessment | subagent | Provides authorized red-team support, recon guidance, and vulnerability assessment planning. |
| `.opencode/agents/cody-the-code-security-analyst.md` | Secure code review | subagent | Reviews code and configuration for security flaws, explains risk, and recommends practical remediation. |
| `.opencode/agents/stacey-the-scripter.md` | Secure scripting | subagent | Helps produce safe, maintainable scripts across common automation languages. |
| `.opencode/agents/logan-the-log-analyst.md` | Log analysis | subagent | Analyzes logs for anomalies, incidents, and likely root causes. |
| `.opencode/agents/casey-the-compliance-analyst.md` | Compliance/governance | subagent | Advises on compliance, control mapping, and governance interpretation. |
| `.opencode/agents/madison-the-cybersecurity-manager.md` | Cybersecurity management | subagent | Assists with practical management planning across policy, staffing, budget, and metrics. |
| `.opencode/agents/cisoinabox.md` | vCISO guidance | primary | Delivers executive-level security strategy, governance guidance, and roadmap support. |

## Command Inventory

| File | Command | Purpose |
| --- | --- | --- |
| `.opencode/commands/search-armis.md` | `/search-armis <query>` | General Armis security search. |
| `.opencode/commands/search-device.md` | `/search-device <identifier>` | Device lookup by hostname, IP, MAC, or other identifier. |
| `.opencode/commands/search-vulnerabilities.md` | `/search-vulnerabilities <criteria>` | Vulnerability-focused search and analysis. |
| `.opencode/commands/sync.md` | `/sync <operation>` | OpenWebUI sync workflow routing. |

## Skill Inventory

| File | Purpose |
| --- | --- |
| `.opencode/skills/operational-framework.md` | Shared operational framework for analysis, investigation, and response tasks. |
| `.opencode/skills/splunk-mcp/SKILL.md` | Routes Splunk requests to the correct MCP workflow. |
| `.opencode/skills/splunk-search/SKILL.md` | Builds, validates, and refines SPL queries. |
| `.opencode/skills/splunk-discovery/SKILL.md` | Discovers indexes, sourcetypes, sources, fields, and lookups. |
| `.opencode/skills/splunk-alert/SKILL.md` | Investigates alerts and validates alert SPL. |
| `.opencode/skills/splunk-savedsearch/SKILL.md` | Discovers, runs, and manages saved searches and reports. |
| `.opencode/skills/splunk-kvstore/SKILL.md` | Discovers and queries KV store collections. |
| `.opencode/skills/splunk-export/SKILL.md` | Extracts larger Splunk result sets with explicit bounds and pagination. |

## Armis Security Analysis Framework

The Armis-focused content follows a repeatable query and validation model.

### Query Strategy

1. Scope clarification: endpoints vs network devices vs all assets.
2. Broad initial query: establish the baseline view.
3. Refined filters: add category, boundary, risk level, or product filters.
4. Result validation: cross-check counts when discrepancies appear.
5. Final analysis: provide actionable findings with confidence scoring.

### Defaults

- Time frames: 7 days for security analysis, 30 days for vulnerability analysis.
- Default scope: endpoints only for security workflows unless clarified otherwise.
- Default boundaries: Corporate and DMZ for security analysis.
- Output threshold: 20 items before switching from terminal output to file output.

### Confidence Scoring

- High: specific query, validated results, clear scope.
- Medium: broad query with minor ambiguity and basic validation.
- Low: very broad query, suspected ambiguity, or possible data quality issues.

## OpenCode Integration Notes

- Use `mode: primary` for durable user-selectable agents.
- Use `mode: subagent` for specialized supporting roles.
- Use `mode: all` only when the agent should be available both directly and as a subagent.
- Keep command routing stable unless there is a clear design reason to change it.
- After changing OpenCode agent, skill, command, plugin, MCP, or config files, tell the user to restart OpenCode for config-time changes to take effect.

## References

- Internal workflows: `docs/internal-workflows.md`
- Prompt style guide: `AGENTIC-SYSTEM-PROMPT-STYLE-GUIDE.md`
- Avatar style guide: `AI-AVATAR-PROMPT-STYLING-GUIDE.md`
- OpenCode Agents: https://opencode.ai/docs/agents/
- OpenCode Commands: https://opencode.ai/docs/commands/
- OpenCode Permissions: https://opencode.ai/docs/permissions/
