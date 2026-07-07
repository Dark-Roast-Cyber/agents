---
name: splunk-kvstore
description: Discover and query Splunk KV store collections via MCP tools.
---

# splunk-kvstore

Use this for KV store discovery, inspection, and read queries.

## MCP Tools

| Tool | Purpose | Risk |
|------|---------|------|
| `splunk_get_kv_store_collections` | List collections and stats | Safe |
| `splunk_run_query` | Query KV store data via `inputlookup`/`outputlookup` | Safe |

## Use it when

- you need to list KV store collections
- you need to inspect collection schema and record counts
- you need to query KV store data for enrichment or correlation
- you need to understand what persistent data is available

## Discovery Workflow

### 1. List all KV store collections

```
splunk_get_kv_store_collections()
```

### 2. Inspect collection structure

```spl
| inputlookup <collection_name> | head 10
```

### 3. Check record count

```spl
| inputlookup <collection_name> | stats count
```

### 4. List field names

```spl
| inputlookup <collection_name> | head 1 | fields *
```

## Query Patterns

### Read all records

```spl
| inputlookup <collection_name>
```

### Filter records

```spl
| inputlookup <collection_name>
| where field_name = "value"
```

### Join KV store with event data

```spl
index=main earliest=-24h
| lookup <collection_name> key_field OUTPUT value_field
| stats count by value_field
```

### Use KV store as an enrichment table

```spl
| inputlookup <collection_name>
| rename key_field AS src_ip
| join type=left src_ip
  [search index=firewall earliest=-24h | stats count by src_ip]
```

### Aggregate KV store data

```spl
| inputlookup <collection_name>
| stats count by category
| sort -count
```

## Common KV Store Use Cases

| Use Case | Pattern |
|----------|---------|
| Asset inventory | `| inputlookup assets \| lookup assets hostname OUTPUT ip, owner` |
| Threat intel | `| inputlookup threat_intel \| search ioc_type=ip` |
| Lookup tables | `| inputlookup geo_mapping \| rename country AS dest_country` |
| Watchlists | `| inputlookup watchlist \| where status="blocked"` |
| CMDB enrichment | `| inputlookup cmdb \| lookup cmdb host OUTPUT app, tier` |

## Safety

- All operations listed here are read-only.
- Writing to KV store (insert, update, delete, truncate) is a destructive write operation not covered by this skill.
- Always use `row_limit` when querying large collections.
- KV store data is app-scoped; verify the correct app context.
