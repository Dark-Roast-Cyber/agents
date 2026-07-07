---
name: splunk-alert
description: Investigate alerts and validate alert SPL via Splunk MCP tools.
---

# splunk-alert

Use this for alert investigation, validation, and setup guidance.

## MCP Tools

| Tool | Purpose | Risk |
|------|---------|------|
| `splunk_get_knowledge_objects` | List existing alerts (type=alerts) | Safe |
| `splunk_run_query` | Validate SPL before creating alerts | Safe |
| `splunk_run_saved_search` | Test-fire an alert on demand | Safe |
| `splunk_get_indexes` | Confirm target index exists | Safe |

## Use it when

- you need to list or inspect configured alerts
- you need to validate alert SPL before creating or modifying an alert
- you need to investigate triggered alert activity
- you need to set up threshold-based alerting

## Alert Investigation Workflow

### 1. List existing alerts

```
splunk_get_knowledge_objects(type="alerts")
```

### 2. Check triggered alert history

```spl
index=_audit action=alert_fired savedsearch_name="<name>"
| table _time, user, savedsearch_name
| sort -_time
```

### 3. Validate alert SPL

Run the alert query with a narrow time window to confirm it works:

```
splunk_run_query(query="<alert SPL>", earliest_time="-1h", row_limit=100)
```

### 4. Test-fire an alert

```
splunk_run_saved_search(saved_search_name="<name>")
```

## Alert Setup Workflow

1. Prototype the detection query with `splunk_run_query` using a narrow time window.
2. Confirm the query returns the expected results or counts.
3. Check for existing alerts with `splunk_get_knowledge_objects(type="alerts")` to avoid duplicates.
4. Create the alert as a saved search with alert actions (write operation, requires confirmation).
5. Verify the alert fires correctly by checking the audit log.

## SPL Patterns for Alerts

### Threshold alert

```spl
index=main sourcetype=app_logs earliest=-5m
| stats count
| where count > 100
```

### Missing data alert

```spl
index=main sourcetype=syslog earliest=-15m
| stats count
| where count = 0
```

### Anomaly baseline

```spl
index=main earliest=-1h
| timechart span=5m count
| eventstats avg(count) as avg_count, stdev(count) as std_count
| where count > (avg_count + 3 * std_count)
```

### Volume drop detection

```spl
index=main earliest=-2h latest=-1h
| stats count as previous_hour
| appendcols
  [search index=main earliest=-1h | stats count as current_hour]
| eval drop_pct = (previous_hour - current_hour) / previous_hour * 100
| where drop_pct > 50
```

## Alert Severity Reference

| Severity | Splunk Value | Typical Use |
|----------|-------------|-------------|
| debug | 1 | Development testing |
| info | 2 | Informational, no action |
| warn | 3 | Default, review needed |
| error | 4 | Action required |
| severe | 5 | Urgent action |
| fatal | 6 | Critical incident |

## Safety

- Listing alerts and validating SPL is read-only.
- Creating or modifying alerts is a write operation. Always validate SPL first.
- Check for duplicate alerts before creating new ones.
- Set alert thresholds to reduce noise; avoid alert storms.
