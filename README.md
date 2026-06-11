# Security Agents

Markdown-first agents, skills, and commands for practical security operations work.

This repository packages specialist AI operating instructions for security teams that need repeatable workflows for asset intelligence, vulnerability analysis, SOC triage, Splunk search, threat intelligence, compliance, secure scripting, code security review, and vCISO-style advisory support.

![Agents in OpenWebUI](./AgentsinOpenWebUI.png)

## What This Project Offers

- **Agents**: durable specialist roles with clear operating rules, scope, safety boundaries, and tool guidance.
- **Skills**: reusable playbooks for repeatable workflows such as Splunk discovery, alert investigation, export, and saved search work.
- **Commands**: slash-style prompts that route common security tasks into the right agent workflow.
- **Local-first source control**: all durable behavior is authored as markdown and can be reviewed like normal code.
- **OpenWebUI publishing support**: optional tooling can publish local agents, skills, and commands to OpenWebUI.

The main goal is simple: keep security automation behavior understandable, reviewable, and portable.

## Included Agents

| Agent | Focus |
| --- | --- |
| `armis-query-agent` | Armis asset, vulnerability, and activity intelligence |
| `splunk-assistant` | Splunk search, discovery, alerts, saved searches, and KV store workflows |
| `soc-analyst` | SOC investigation and incident analysis |
| `sonny-the-soc-analyst` | Verdict-oriented SOC triage |
| `tim-the-threat-intel-analyst` | Threat intelligence analysis |
| `john-anderton-procog-analyst-clone` | IOC, actor, campaign, and TTP research |
| `ai-nyx-the-red-teamer` | Authorized red-team and vulnerability assessment support |
| `cody-the-code-security-analyst` | Secure code review and remediation guidance |
| `stacey-the-scripter` | Safe Bash, Python, and PowerShell scripting support |
| `casey-the-compliance-analyst` | Compliance, governance, and control mapping |
| `madison-the-cybersecurity-manager` | Cybersecurity management planning |
| `cisoinabox` | vCISO-style strategy and program guidance |
| `logan-the-log-analyst` | Log analysis, anomaly review, and root-cause support |

Agent definitions live in `.opencode/agents/`.

## Included Commands

| Command | Purpose |
| --- | --- |
| `/search-armis <query>` | Search Armis from a natural-language request |
| `/search-device <identifier>` | Look up a device by hostname, IP, MAC address, or other identifier |
| `/search-vulnerabilities <criteria>` | Search and analyze vulnerabilities |
| `/sync <operation>` | Manage local-to-OpenWebUI sync workflows |

Command definitions live in `.opencode/commands/`.

## Included Skills

| Skill | Purpose |
| --- | --- |
| `operational-framework` | Shared operating model for concise, evidence-based analysis |
| `splunk-mcp` | Router for Splunk MCP workflows |
| `splunk-search` | Build and validate Splunk SPL queries |
| `splunk-discovery` | Discover Splunk indexes, sourcetypes, sources, fields, and lookups |
| `splunk-alert` | Investigate alerts and validate alert SPL |
| `splunk-savedsearch` | Discover, run, and manage saved searches and reports |
| `splunk-kvstore` | Discover and query KV store collections |
| `splunk-export` | Extract larger Splunk result sets with explicit bounds and pagination |

Skill definitions live in `.opencode/skills/`.

## Repository Layout

```text
.opencode/
  agents/      # Specialist agent definitions
  commands/    # Slash-style prompt shortcuts
  skills/      # Reusable workflow playbooks
  images/      # Optional agent avatar assets
openwebui/     # Optional OpenWebUI sync and API tooling
docs/          # Internal workflow documentation
README.md      # Public project overview
AGENTS.md      # AI coding-tool guidance
```

## Typical Use Cases

- Search and interpret Armis asset or vulnerability data.
- Build and validate bounded Splunk searches.
- Triage SOC alerts with consistent evidence handling.
- Summarize threat intelligence and indicators.
- Review code or scripts for security issues.
- Map security work to compliance and management concerns.
- Maintain a version-controlled catalog of reusable security AI behavior.

## Documentation

- `AGENTS.md` is the AI-facing project guide for coding agents and automation tools.
- `docs/internal-workflows.md` documents local authoring, agent creation, and OpenWebUI sync workflows.
- `AGENTIC-SYSTEM-PROMPT-STYLE-GUIDE.md` documents prompt and agent-instruction style guidance.
- `AI-AVATAR-PROMPT-STYLING-GUIDE.md` documents avatar prompt conventions.

## Project Model

This repo treats markdown files as the source of truth. OpenCode is the primary authoring environment, and OpenWebUI is an optional publishing target. That separation keeps agent behavior transparent, auditable, and easy to change through normal pull-request review.
