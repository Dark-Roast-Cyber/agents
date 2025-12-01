# Armis and SOC Agent Configuration Update

## Summary of Changes

### ✅ Updated Files

#### Project-Specific Agents (`/home/christian/github/agents/`)
1. **`armis-query-agent.md`** - Enhanced with smart output handling
2. **`armis-query.md`** - Updated command description
3. **`soc-analyst.md`** - Added Armis integration and write capabilities

#### Project-Specific Agents (`.opencode/agent/`)
1. **`armis-query-agent.md`** - Enhanced with smart output handling
2. **`soc-analyst.md`** - Added Armis integration and write capabilities

#### Global Configuration (`/home/christian/.config/opencode/`)
1. **`tools.json`** - Added Armis MCP tools
2. **`config.json.armis`** - Added Armis MCP tools

## Key Enhancements

### 🧠 Smart Output Handling
- **Automatic Decision Making**: No parameters needed
- **≤ 20 items**: Display directly in terminal
- **> 20 items**: Write to timestamped JSON file
- **Clear Communication**: Always inform user of output location

### 🔧 Tool Permissions
- **Armis Agent**: Added `write: true` for file output
- **SOC Analyst**: Added `write: true` and Armis access
- **Global Config**: Enabled Armis MCP tools across all agents

### 📁 File Naming Convention
- Armis Agent: `armis_results_YYYY-MM-DD_HHMMSS.json`
- SOC Analyst: `soc_armis_results_YYYY-MM-DD_HHMMSS.json`

### 🎯 Enhanced Capabilities
- **SOC Analyst**: Now integrates Armis for asset context in investigations
- **Cross-Tool Integration**: SOC can leverage Armis during incident response
- **Structured JSON Output**: Consistent format for all file outputs

## Usage Examples

### Before (Manual Parameters)
```bash
armis-query "CentOS devices" --output-file=results.json --format=json
```

### After (Smart & Automatic)
```bash
armis-query "CentOS devices"
# Agent automatically decides output format based on result size
```

## Benefits

1. **No Parameters to Remember**: Agents make intelligent decisions
2. **Context-Aware**: Output format adapts to result size
3. **Consistent Experience**: Same behavior across all agents
4. **Enhanced SOC Capabilities**: Security analysts now have asset intelligence
5. **Structured Data**: JSON format for easy processing and analysis

## File Output Format
```json
{
  "query": "ASQ query used",
  "timestamp": "2025-11-30T19:44:31Z",
  "total_results": 59,
  "summary": "Brief description of findings",
  "devices": [...]
}
```

All agents and tools have been successfully updated with the smart, context-aware approach!