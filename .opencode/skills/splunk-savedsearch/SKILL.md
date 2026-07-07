---
name: splunk-savedsearch
description: Discover, run, and manage Splunk saved searches and reports via MCP tools.
---

# splunk-savedsearch

Use this for saved search and report workflows.

## MCP Tools

| Tool | Purpose | Risk |
|------|---------|------|
| `splunk_get_knowledge_objects` | List saved searches (type=saved_searches) | Safe |
| `splunk_run_saved_search` | Execute an existing saved search by name | Safe |
| `splunk_run_query` | Prototype SPL before creating saved searches | Safe |

## Use it when

- you need to list or inspect saved searches
- you need to run a saved search on demand
- you need to prototype SPL before creating a saved search
- you need to check what reports already exist to avoid duplicates

## Workflow

### 1. Discover existing saved searches

```
splunk_get_knowledge_objects(type="saved_searches")
```

### 2. Run a saved search on demand

```
splunk_run_saved_search(saved_search_name="<name>")
```

### 3. Prototype before creating

Always validate SPL with `splunk_run_query` before creating a saved search:

```spl
index=main earliest=-24h | stats count by sourcetype | sort -count
```

Run this as a bounded query first, then promote to a saved search only after confirming the results.

## SPL Patterns for Reports

### Daily summary

```spl
index=main earliest=-24h
| stats count, dc(host) as hosts by sourcetype
| sort -count
```

### Top talkers

```spl
index=network earliest=-24h
| stats sum(bytes) as total_bytes by src_ip
| sort -total_bytes
| head 20
```

### Error rate over time

```spl
index=main sourcetype=app_logs earliest=-7d
| timechart span=1d count by status
```

### Scheduled search validation

After creating a saved search, verify it runs:

```
splunk_run_saved_search(saved_search_name="<name>")
```

Check the audit log for execution history:

```spl
index=_internal sourcetype=scheduler savedsearch_name="<name>"
| table _time, status, run_time, result_count
```

## Safety

- Listing and running saved searches is read-only.
- Creating or modifying saved searches is a write operation. Validate SPL first with `splunk_run_query`.
- Do not create duplicate saved searches. Check with `splunk_get_knowledge_objects` first.
- Ensure schedule intervals are appropriate to avoid search load.
