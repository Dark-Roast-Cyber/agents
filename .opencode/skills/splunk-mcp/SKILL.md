---
name: splunk-mcp
description: Router skill that maps Splunk requests to the correct MCP tool and workflow.
---

# splunk-mcp

Use this first when a request is about Splunk and the right workflow is not obvious.

## MCP Tools

| Tool | Purpose | Risk |
|------|---------|------|
| `splunk_run_query` | Execute SPL search | Safe |
| `splunk_get_metadata` | Discover hosts, sources, sourcetypes | Safe |
| `splunk_get_indexes` | List available indexes | Safe |
| `splunk_get_index_info` | Index size, retention, event count | Safe |
| `splunk_run_saved_search` | Execute an existing saved search | Safe |
| `splunk_get_knowledge_objects` | List saved searches, alerts, dashboards | Safe |
| `splunk_get_kv_store_collections` | List KV store collections and stats | Safe |
| `splunk_get_info` | Splunk instance info | Safe |
| `splunk_get_user_info` | Current user details and roles | Safe |
| `splunk_get_user_list` | List Splunk users | Safe |

## Routing

| Intent | MCP Tool | Skill |
|--------|----------|-------|
| Run a query | `splunk_run_query` | `splunk-search` |
| Discover indexes, sourcetypes, fields | `splunk_get_metadata` | `splunk-discovery` |
| Index details or health | `splunk_get_index_info` | `splunk-discovery` |
| Run or manage saved searches | `splunk_run_saved_search`, `splunk_get_knowledge_objects` | `splunk-savedsearch` |
| Investigate or create alerts | `splunk_get_knowledge_objects` (type=alerts) | `splunk-alert` |
| KV store data | `splunk_get_kv_store_collections` | `splunk-kvstore` |
| Large result extraction | `splunk_run_query` with pagination | `splunk-export` |
| Instance or user info | `splunk_get_info`, `splunk_get_user_info` | inline |

## Default Workflow

1. Verify connection with `splunk_get_info` if the environment may be the issue.
2. Prefer read-only discovery before mutation.
3. Choose the narrowest specialized skill that fits.
4. Always include explicit time bounds and `row_limit` on queries.
5. Validate SPL by running a bounded `splunk_run_query` before committing to saved searches or alerts.

## SPL Construction Guidance

When using generative AI to write SPL:

1. Start with the smallest query that answers the question.
2. Include `earliest_time` and `latest_time` on every query.
3. Use `row_limit` to cap result sets (default 100, max 1000).
4. Use `| head N`, `| stats count`, or `| fields` to bound output before expanding.
5. If a query returns zero results, check time range and metadata assumptions before adding complexity.
6. Validate non-trivial SPL with a bounded run before creating saved searches or alerts.
7. Prefer specific indexes and sourcetypes over broad searches.

## Context Management

To reduce cold starts and repetitive discovery:

1. Use `splunk_get_info` to confirm the environment.
2. Use `splunk_get_indexes` to build an index inventory.
3. Use `splunk_get_metadata` to map sourcetypes per index.
4. Cache these results in the conversation context.
5. Only re-query metadata when the environment may have changed.

## Safety

- All MCP tools listed above are read-only by default.
- Write operations (creating saved searches, alerts, or KV store records) require explicit confirmation.
- Never include credentials, tokens, or secrets in SPL queries.
- Always scope queries with explicit time bounds to avoid full index scans.
