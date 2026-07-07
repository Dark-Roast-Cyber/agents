---
name: splunk-export
description: Extract larger Splunk result sets with explicit bounds and pagination using MCP tools.
---

# splunk-export

Use this when you need to extract larger result sets from Splunk.

## MCP Tools

| Tool | Purpose | Risk |
|------|---------|------|
| `splunk_run_query` | Execute SPL with pagination via row_limit and offset | Safe |

## Use it when

- you need more results than a typical ad-hoc query returns
- you need to paginate through large result sets
- you need structured data extraction for downstream processing

## Extraction Workflow

### 1. Estimate result count first

```spl
index=<index> sourcetype=<type> earliest=-7d | stats count
```

Run with `splunk_run_query(row_limit=1000)` to get the count.

### 2. Extract with pagination

Use `splunk_run_query` with increasing `offset` values:

```
splunk_run_query(query="...", earliest_time="-7d", row_limit=1000, offset=0)
splunk_run_query(query="...", earliest_time="-7d", row_limit=1000, offset=1000)
splunk_run_query(query="...", earliest_time="-7d", row_limit=1000, offset=2000)
```

### 3. Reduce field set for efficiency

```spl
index=<index> earliest=-7d
| fields _time, host, status, uri
| sort _time
```

Use `| fields` to select only the columns needed for the downstream task.

## Export Patterns

### Bounded extraction

```spl
index=<index> earliest=-24h
| fields host, status, uri, bytes
| sort _time
| head 5000
```

### Aggregated export

Instead of raw events, export aggregates to reduce volume:

```spl
index=<index> earliest=-7d
| stats count, avg(bytes) as avg_bytes, dc(uri) as unique_uris by host, status
| sort -count
```

### Time-bucketed extraction

```spl
index=<index> earliest=-30d
| bin _time span=1d
| stats count by _time, sourcetype
| sort _time
```

### Selective field export

```spl
index=main earliest=-24h
| table _time, host, src_ip, status, uri, user_agent
| sort _time
```

## Best Practices

1. **Estimate first.** Run `| stats count` before extracting large result sets.
2. **Use explicit time bounds.** Never run unbounded exports.
3. **Reduce fields.** Use `| fields` or `| table` to select only needed columns.
4. **Prefer aggregates.** Export `| stats` output instead of raw events when possible.
5. **Paginate large sets.** Use `row_limit` and `offset` for controlled extraction.
6. **Sort deterministically.** Use `| sort _time` or another field to ensure consistent pagination.

## Safety

- All export operations are read-only.
- Always include `earliest_time` and `latest_time` on export queries.
- Use `row_limit` to prevent runaway result sets.
- Be mindful of downstream data handling; do not export sensitive fields unnecessarily.
