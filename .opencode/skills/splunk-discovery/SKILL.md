---
name: splunk-discovery
description: Discover indexes, sourcetypes, sources, fields, and lookups before writing SPL.
---

# splunk-discovery

Use this before or during SPL authoring to understand what data is available.

## MCP Tools

| Tool | Purpose | Risk |
|------|---------|------|
| `splunk_get_indexes` | List available indexes | Safe |
| `splunk_get_index_info` | Index size, event count, time range, retention | Safe |
| `splunk_get_metadata` | Discover hosts, sources, sourcetypes | Safe |
| `splunk_run_query` | Field discovery and sample events | Safe |

## Use it when

- you need to list indexes or confirm an index exists
- you need sources or sourcetypes for a dataset
- you need field discovery or metadata-based pivots
- you are writing SPL against an unfamiliar environment
- a query returns zero results and you need to verify assumptions

## Discovery Workflow

1. Confirm the target index exists: `splunk_get_indexes`
2. Check index health and time range: `splunk_get_index_info(index_name="<index>")`
3. Discover sourcetypes: `splunk_get_metadata(type="sourcetypes", index="<index>")`
4. Discover sources: `splunk_get_metadata(type="sources", index="<index>")`
5. Discover hosts: `splunk_get_metadata(type="hosts", index="<index>")`
6. Inspect fields and sample data with `splunk_run_query`

## Field Discovery Patterns

### List all fields in an index

```spl
index=<index> | head 1 | fields *
```

### Field summary with coverage

```spl
index=<index> | fieldsummary maxvals=10
| where count > 0
| table field, count, distinct_count, coverage
```

### Sample events for shape inspection

```spl
index=<index> sourcetype=<type> | head 10
```

### Discover unique values for a field

```spl
index=<index> | top <field> limit=20
```

### Check time range of available data

```spl
index=<index> | stats min(_time) as earliest, max(_time) as latest
```

### Sourcetype volume

```spl
index=<index> | stats count by sourcetype | sort -count
```

## Lookup Discovery

Lookups are enrichment tables that join external data into search results.

### List available lookups

Use `splunk_run_query` with:

```spl
| inputlookup <lookup_name> | head 10
```

### Check lookup field structure

```spl
| inputlookup <lookup_name> | head 1 | fields *
```

### Use a lookup in a search

```spl
index=<index> earliest=-24h
| lookup <lookup_name> <input_field> OUTPUT <output_field>
```

## Common Pitfalls

- **Zero results:** Check if the index name, sourcetype, or time range is wrong.
- **Missing fields:** Fields may not exist in all sourcetypes. Use `| fields *` to inspect.
- **Stale metadata:** `splunk_get_metadata` reflects current data; if no recent events exist, the sourcetype may not appear.
- **Case sensitivity:** Sourcetype and field names are case-sensitive in Splunk.

## Safety

- All discovery operations are read-only.
- Use narrow time ranges for field summary queries to avoid scanning the full index.
- Use `row_limit` when querying sample events.
