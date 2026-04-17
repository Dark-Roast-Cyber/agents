# Armis Security Agents Project

This repository manages OpenCode-first security operations assets: agents, skills, and slash commands authored as local markdown and synced to OpenWebUI when needed. It is primarily focused on Armis-driven security workflows, but it also includes broader security personas for SOC operations, CTI, compliance, code review, scripting, management, and executive guidance.

The repo is designed around a simple principle: author locally, validate locally, and publish outward to OpenWebUI as a distribution target.

## Project Overview

- **Primary purpose**: maintain OpenCode agents, skills, and commands for security operations
- **Authoring model**: local markdown files in this repo are the source of truth
- **Publishing target**: OpenWebUI models, skills, and prompts
- **Operational focus**: Armis asset intelligence, vulnerability workflows, SOC analysis, and adjacent security functions
- **Tooling included**: a local `openwebui` Python package and CLI for planning, pushing, importing, and exploring OpenWebUI content

## Project Structure

```text
/
├── .opencode/
│   ├── agents/
│   │   ├── armis-query-agent.md
│   │   ├── soc-analyst.md
│   │   ├── ai-nyx-the-red-teamer.md
│   │   ├── john-anderton-procog-analyst-clone.md
│   │   ├── cisoinabox.md
│   │   ├── cody-the-code-security-analyst.md
│   │   ├── stacey-the-scripter.md
│   │   ├── logan-the-log-analyst.md
│   │   ├── madison-the-cybersecurity-manager.md
│   │   ├── casey-the-compliance-analyst.md
│   │   └── sonny-the-soc-analyst.md
│   ├── commands/
│   │   ├── search-armis.md
│   │   ├── search-device.md
│   │   └── search-vulnerabilities.md
│   ├── skills/
│   │   └── README.md
│   └── package.json
├── openwebui/
│   ├── __init__.py
│   ├── pyproject.toml
│   ├── cli.py
│   ├── client.py
│   ├── sync.py
│   ├── opencode.py
│   ├── models.py
│   ├── prompts.py
│   ├── skills.py
│   ├── functions.py
│   ├── tools.py
│   ├── knowledge.py
│   └── chat.py
├── AGENTS.md
└── .gitignore
```

## OpenCode ↔ OpenWebUI Sync

### Sync Philosophy

- This repo is the **source of truth** for OpenCode-first authoring.
- OpenWebUI is a **publish/import target**, not the primary editing surface.
- v1 sync is **overwrite-oriented**: push local markdown outward, or import tagged remote assets inward.
- v1 does **not** attempt bidirectional merge, conflict resolution, or delete propagation.
- Import remote models only when `meta.tags` contains a tag object with `name == "drc-agent"`.
- Ignore bulky UI-only fields during import/export, except preserve `meta.profile_image_url` when present so agent images survive sync.

### Object Mapping

- **Agent** → OpenWebUI **Workspace Model**
- **Skill** → OpenWebUI **Skill**
- **Command** → OpenWebUI **Prompt**

### Naming Rules

- The filename slug is the canonical id.
- Display name defaults to the titleized filename slug.
- Example: `armis-query-agent.md` → `Armis Query Agent`

## When to Create an Agent vs Skill vs Command

Use the smallest durable abstraction that matches the job.

### Create an Agent when

- You need a durable persona or long-lived system behavior
- The artifact represents something a user would plausibly select as a model
- The behavior should carry its own identity, permissions, tone, and operating rules

### Create a Skill when

- You need reusable instructions or a playbook
- The content should be attached or invoked on demand
- The content is guidance or workflow, not identity

### Create a Command when

- You need a slash-style shortcut
- You are wrapping a common task or workflow
- You want a prompt template that routes work into an agent consistently

## Agent Inventory

The repository currently contains 12 agents.

| File | Purpose | Mode | Description |
| --- | --- | --- | --- |
| `.opencode/agents/armis-query-agent.md` | Primary Armis ASQ query agent | primary | Translates natural-language security requests into validated Armis Standard Query workflows. |
| `.opencode/agents/soc-analyst.md` | SOC analysis | subagent | Supports SOC investigations and security analysis tasks. |
| `.opencode/agents/ai-nyx-the-red-teamer.md` | Red team/vuln assessment | subagent | Provides authorized red-team support, recon guidance, and vulnerability assessment planning. |
| `.opencode/agents/john-anderton-procog-analyst-clone.md` | CTI/IOC research | subagent | Summarizes IOCs, actors, campaigns, and TTPs for concise CTI workflows. |
| `.opencode/agents/cisoinabox.md` | vCISO guidance | primary | Delivers executive-level security strategy, governance guidance, and roadmap support. |
| `.opencode/agents/cody-the-code-security-analyst.md` | Secure code review | subagent | Reviews code and configuration for security flaws, explains risk, and recommends practical remediation. |
| `.opencode/agents/stacey-the-scripter.md` | Secure scripting | subagent | Helps produce safe, maintainable scripts across common automation languages. |
| `.opencode/agents/logan-the-log-analyst.md` | Log analysis | subagent | Analyzes logs for anomalies, incidents, and likely root causes. |
| `.opencode/agents/madison-the-cybersecurity-manager.md` | Cybersecurity management | subagent | Assists with practical management planning across policy, staffing, budget, and metrics. |
| `.opencode/agents/casey-the-compliance-analyst.md` | Compliance/governance | subagent | Advises on compliance, control mapping, and governance interpretation. |
| `.opencode/agents/sonny-the-soc-analyst.md` | SOC triage | subagent | Provides verdict-oriented alert triage and next-step guidance for investigations. |
| `.opencode/agents/tim-the-threat-intel-analyst.md` | Threat intelligence analysis | subagent | Performs CTI analysis on threat reports, indicators, campaigns, and threat actors using Polarity and ThreatConnect tools. |

## Command Inventory

All current commands route into `armis-query-agent` and are configured with `subtask: false` to preserve the primary session context.

- `/search-armis <query>` — general Armis security search
- `/search-device <identifier>` — device lookup by hostname, IP, MAC, or other identifier
- `/search-vulnerabilities <criteria>` — vulnerability-focused search and analysis

## Skills

The repo includes a repo-local skills directory at `.opencode/skills/` for markdown-based reusable skills.

- Skills are intended for reusable instruction sets and playbooks
- Skills are not standalone personas
- Skills should be authored as single markdown files in `.opencode/skills/*.md`

## Sync Tooling

The `openwebui` Python package provides CLI support for sync operations and direct API exploration.

### Sync Commands

- `python -m openwebui sync plan` — read-only sync preview
- `python -m openwebui sync push agents` — push agents to OpenWebUI
- `python -m openwebui sync push commands` — push commands to OpenWebUI
- `python -m openwebui sync push skills` — push skills to OpenWebUI
- `python -m openwebui sync push all` — push everything
- `python -m openwebui sync import agents` — import tagged models from OpenWebUI

### Other CLI Commands

- `python -m openwebui models list`
- `python -m openwebui models get <id>`
- `python -m openwebui models create --id <id> --name <name> [--base-model ...] [--description ...] [--system-prompt ...]`
- `python -m openwebui models delete <id>`
- `python -m openwebui models export`
- `python -m openwebui tools list`
- `python -m openwebui functions list`
- `python -m openwebui prompts list`
- `python -m openwebui skills list`
- `python -m openwebui knowledge list`
- `python -m openwebui chat --model <model> --message <message>`

### Practical Usage Notes

- Run sync tooling intentionally; push operations are publish actions, not dry runs
- Use `sync plan` before `sync push` when validating a release
- Use `sync import agents` only for remote models intentionally tagged `drc-agent`
- Keep local markdown clean and reviewable before pushing outward

## Security Analysis Framework

The Armis-focused content in this repo follows a repeatable query and validation model.

### Query Strategy

1. **Scope Clarification** — endpoints vs network devices vs all assets
2. **Broad Initial Query** — establish the baseline view
3. **Refined Filters** — add category, boundary, risk level, or product filters
4. **Result Validation** — cross-check counts when discrepancies appear
5. **Final Analysis** — provide actionable findings with confidence scoring

### Default Parameters

- **Time frames**: 7 days for security analysis, 30 days for vulnerability analysis
- **Default scope**: endpoints only for security workflows unless clarified otherwise
- **Default boundaries**: Corporate + DMZ for security analysis
- **Output threshold**: 20 items before switching from terminal output to file output

### Confidence Scoring

- **High** — specific query, validated results, clear scope
- **Medium** — broad query with minor ambiguity and basic validation
- **Low** — very broad query, suspected ambiguity, or possible data quality issues

## Smart Query Templates

### Unprotected Endpoints

```asq
in:devices timeFrame:"7 Days" category:Computers boundary:Corporate,DMZ !dataSource:(name:CrowdStrike,SentinelOne,"Microsoft Defender")
```

### Critical Risk Devices

```asq
in:devices timeFrame:"7 Days" category:Computers riskLevel:Critical
```

### Security Software Inventory

```asq
in:devices timeFrame:"7 Days" application:(name:"CrowdStrike" OR name:"SentinelOne")
```

## File Output Format

Large result sets should be written to timestamped JSON with structured metadata.

```json
{
  "query": "ASQ query used",
  "timestamp": "2025-11-30T19:44:31Z",
  "total_results": 59,
  "confidence_score": "High",
  "data_quality": "Validated",
  "scope": "Corporate+DMZ endpoints only",
  "summary": "Brief description of findings",
  "risk_distribution": {},
  "validation_notes": "Cross-checked with alternative query method"
}
```

## Error Recovery and Validation

### Common Clarifications

- Is the identifier a hostname, IP address, MAC address, or device ID?
- Should the search target devices, vulnerabilities, or activities?
- What time frame should be used?
- Should the scope be endpoints only, network devices, or all assets?
- Should the search include Corporate, DMZ, or both?

### Validation Checks

- Cross-check query results when counts appear inconsistent
- Validate device counts through alternate query constructions
- Confirm vendor naming variations when checking security products
- Call out uncertainty instead of overstating confidence

## OpenCode Integration Notes

### Permission Model

- **Armis MCP**: `allow` for security operations
- **Write**: `ask` for file modifications where needed
- **Read**: `allow` for local analysis
- **Webfetch**: `ask` for external documentation lookup

### Agent Mode Expectations

- Use **primary** mode for durable user-selectable agents
- Use **subagent** mode for specialized supporting roles
- Keep command routing stable unless there is a clear design reason to change it

## Development Guidelines

### Adding a New Agent

1. Create a markdown file in `.opencode/agents/`
2. Use the filename slug as the canonical id
3. Add clear frontmatter, typically including:
   - `description`
   - `mode`
   - `temperature`
   - `permission`
4. Use `permission`, not the deprecated `tools` field
5. Write concise, durable instructions that define identity, scope, and operating rules
6. Update this `AGENTS.md` inventory and any relevant sync documentation

### Adding a New Skill

1. Create a markdown file in `.opencode/skills/`
2. Keep it reusable and identity-free
3. Focus on workflow, policy, or repeatable instructions
4. Name it clearly so its purpose is obvious from the slug
5. Update this guide if the skill becomes part of the standard project workflow

### Adding a New Command

1. Create a markdown file in `.opencode/commands/`
2. Set `agent: <agent-slug>` to define routing
3. Set `subtask: false` unless there is a deliberate reason to isolate context
4. Keep the body short and task-oriented
5. Follow established error recovery and scope clarification patterns
6. Update the command inventory in this file

### Naming Conventions

- Prefer lowercase kebab-case filenames
- Treat the filename slug as canonical across sync workflows
- Let the display name default to the titleized slug unless there is a strong reason to override it
- Avoid duplicate concepts unless retaining a legacy compatibility entry intentionally

### Armis-Specific Guidance

- Maintain `temperature: 0.1` for deterministic security analysis where applicable
- Preserve the query validation and confidence-scoring framework
- Keep endpoint-vs-network scope clarification explicit
- Document major capability changes in this file

## Testing and Validation

### Recommended Test Scenarios

1. **Unprotected endpoint search** — verify network device exclusion
2. **Critical vulnerability analysis** — test risk prioritization
3. **Device lookup by hostname** — validate multi-field search behavior
4. **Security software inventory** — test vendor name variations
5. **Large result sets** — verify file output formatting and summaries

### Quality Checks

- Cross-check query results with alternate methods
- Validate confidence scoring against query specificity
- Test error recovery with ambiguous input
- Verify file output format consistency
- Confirm the permission model still matches intended usage

## External Dependencies and References

### MCP Integration

- **Armis Security Remote MCP** is the primary data source for Armis security workflows
- Wildcard permissions use the `armis-security-remote-mcp_*` pattern

### References

- OpenCode Agents: https://opencode.ai/docs/agents/
- OpenCode Commands: https://opencode.ai/docs/commands/
- OpenCode Permissions: https://opencode.ai/docs/permissions/

## Version History

### v2.4 (2026-04-16)
- Rewrote `AGENTS.md` into a comprehensive project guide with clearer structure and navigation
- Added explicit OpenCode ↔ OpenWebUI sync mapping for agents, skills, and commands
- Documented the local `openwebui` Python package and CLI sync workflows in one place
- Expanded project structure, inventory, and development guidance while preserving Armis operational content

### v2.3 (2026-04-16)
- Imported 10 `drc-agent` tagged models from OpenWebUI into `.opencode/agents/`
- Added the `drc-agent` tag to 9 AI Team models in OpenWebUI for sync eligibility
- Improved imported agents with proper OpenCode frontmatter, including `temperature`, `permission`, and `mode`
- Pushed all local agents back to OpenWebUI using the repo sync tooling
- Documented that `ai-cody-the-code-security-analyst-.md` (trailing hyphen) is superseded by `ai-cody-the-code-security-analyst-frontier.md`

### v2.2 (2026-04-16)
- Added minimal OpenCode/OpenWebUI sync guidance for agents, skills, and commands
- Added repo-local `.opencode/skills/` convention for markdown-based skills
- Added Python sync tooling for plan, push, and tagged-agent import workflows

### v2.1 (2026-04-15)
- Migrated agent directory from `.opencode/agent/` to `.opencode/agents/` (OpenCode convention)
- Migrated command directory from `.opencode/command/` to `.opencode/commands/` (OpenCode convention)
- Replaced deprecated `tools` frontmatter with `permission` in all agent files
- Removed root-level backup files (`armis-query-agent.md`, `armis-query.md`, `soc-analyst.md`)
- Removed stale documentation files (improvements summary, compliance report, etc.)
- Updated `AGENTS.md` to reflect the cleaned-up project structure

### v2.0 (2025-11-30)
- Enhanced with OpenCode best practices
- Added temperature and permission configuration
- Improved error recovery and validation framework
- Added confidence scoring and data quality indicators
- Integrated smart query templates
- Enhanced file output format with metadata
- Comprehensive command implementation

### v1.0 (Initial)
- Basic Armis query agent functionality
- Simple command structure
- Core ASQ translation capabilities
