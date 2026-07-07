---
name: splunk-search
description: Build, validate, and iteratively refine SPL queries using the Splunk MCP server.
---

# splunk-search

Use this for SPL construction, validation, and iterative query building.

## MCP Tools

| Tool | Purpose | Risk |
|------|---------|------|
| `splunk_run_query` | Execute SPL with time bounds and row limit | Safe |

## Use it when

- you need to build or refine an SPL query
- you need to validate SPL before creating a saved search or alert
- you need ad-hoc investigation results
- you need to test query shape and volume before expanding scope

## Iterative Query Workflow

1. Start with discovery (use `splunk-discovery` if index/sourcetype/fields are unknown).
2. Draft the smallest SPL that can answer the question.
3. Run a bounded test: `splunk_run_query(query="...", earliest_time="-1h", row_limit=100)`.
4. If zero results, check time range, index, and sourcetype assumptions.
5. If shape is wrong, add `| stats`, `| table`, or `| where` to refine.
6. Only expand time range or `row_limit` after the query is proven.
7. For recurring use, promote to a saved search via `splunk-savedsearch`.

## SPL Construction Patterns

### Start small

```spl
index=main sourcetype=syslog earliest=-1h | head 20
```

### Confirm volume

```spl
index=main sourcetype=syslog earliest=-24h | stats count
```

### Shape the output

```spl
index=main sourcetype=syslog earliest=-24h
| stats count by host, sourcetype
| sort -count
```

### Add time context

```spl
index=main earliest=-7d
| timechart span=1h count by sourcetype
```

### Field filtering

```spl
index=main earliest=-24h
| fields host, status, uri
| table host status uri
| where status >= 400
```

### Subsearch

```spl
index=main earliest=-24h
  [search index=alerts earliest=-1h | fields src_ip | head 100]
| stats count by src_ip
```

## Validation Checklist

Before expanding a query or promoting to a saved search:

- Does the SPL parse without error? Run with a narrow time window first.
- Is the index correct? Verify with `splunk_get_indexes` or `splunk_get_index_info`.
- Is the sourcetype correct? Verify with `splunk_get_metadata(type="sourcetypes")`.
- Are the fields available? Verify with `splunk_get_metadata` or `| fieldsummary`.
- Is the time range appropriate? Use the narrowest range that answers the question.
- Is the result set bounded? Use `row_limit`, `| head`, or `| stats count`.

## Recovery Ladder

When a query returns unexpected results:

1. Simplify the SPL. Remove pipes, keep `index=X | head 10`.
2. Confirm index and sourcetype with `splunk_get_metadata`.
3. Inspect fields with `| fieldsummary` or `| head 1 | fields *`.
4. Widen time bounds deliberately.
5. Check for typos in field names or values.

## SPL Command Quick Reference

| Command | Purpose |
|---------|---------|
| `stats` | Aggregate (count, sum, avg, dc, values) |
| `timechart` | Time-series aggregation |
| `table` | Select specific fields |
| `where` | Filter results |
| `eval` | Create computed fields |
| `sort` | Order results |
| `head` / `tail` | Limit result count |
| `fields` | Include or exclude fields |
| `dedup` | Remove duplicates |
| `rex` | Regex field extraction |
| `lookup` | Enrich from lookup tables |
| `mvexpand` | Expand multivalue fields |
| `foreach` | Iterate over field sets |

## Safety

- Read-only by default.
- Always include `earliest_time` and `latest_time`.
- Use `row_limit` to prevent runaway result sets.
- Treat `| outputlookup`, `| collect`, `| delete`, and `| sendalert` as high-risk write operations.
