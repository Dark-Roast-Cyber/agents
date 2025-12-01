# Armis Security Agents Project

This project contains specialized OpenCode agents and commands for Armis security operations, including asset intelligence, vulnerability management, and security analysis.

## Project Structure

```
/
├── .opencode/
│   ├── agent/
│   │   ├── armis-query-agent.md     # Primary Armis security query agent
│   │   └── soc-analyst.md           # Security operations center analyst
│   └── command/
│       ├── search-armis.md          # General Armis search command
│       ├── search-device.md         # Device-specific search command
│       └── search-vulnerabilities.md # Vulnerability search command
├── AGENTS.md                        # This file - Main project documentation
├── ARMIS_AGENT_IMPROVEMENTS_SUMMARY.md  # Detailed enhancement summary
├── COMMAND_IMPLEMENTATION.md        # Command implementation details
├── OPENCODE_COMPLIANCE_REPORT.md    # OpenCode compliance validation
├── UPDATE_SUMMARY.md               # Configuration update summary
├── armis-query-agent.md            # Root-level agent backup
├── armis-query.md                  # Legacy command
├── soc-analyst.md                  # Root-level agent backup
└── .gitignore
```

## Agent Configuration

### Primary Agent: Armis Query Agent
- **File**: `.opencode/agent/armis-query-agent.md`
- **Purpose**: Translates natural language to Armis Standard Query (ASQ)
- **Temperature**: 0.1 (focused, deterministic)
- **Tools**: Armis MCP, write (ask), read, webfetch (ask)
- **Specialization**: Security analysis with validation and confidence scoring

### Subagent: SOC Analyst
- **File**: `.opencode/agent/soc-analyst.md`
- **Purpose**: Security operations center analysis
- **Mode**: Subagent for specialized security tasks

## Command Configuration

All commands are configured to use the `armis-query-agent` and are set with `subtask: false` to maintain context in the primary session.

### Available Commands
- `/search-armis <query>` - General Armis security search
- `/search-device <identifier>` - Specific device lookup
- `/search-vulnerabilities <criteria>` - Vulnerability analysis

## Security Analysis Framework

### Query Strategy
1. **Scope Clarification** - Endpoints vs network devices vs all assets
2. **Broad Initial Query** - Get baseline understanding
3. **Refined Filters** - Add category, boundary, risk level filters
4. **Result Validation** - Cross-check counts if discrepancies suspected
5. **Final Analysis** - Actionable insights with confidence scores

### Default Parameters
- **Time frames**: 7 days (security), 30 days (vulnerabilities)
- **Scope**: Endpoints only for security analysis
- **Boundaries**: Corporate+DMZ for security analysis
- **Output threshold**: 20 items for file vs terminal display

### Confidence Scoring
- **High**: Specific query with validated results, clear scope
- **Medium**: Broad query with some ambiguity, basic validation
- **Low**: Very broad query, suspected data quality issues

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

Results are written to timestamped JSON files with enhanced metadata:
```json
{
  "query": "ASQ query used",
  "timestamp": "2025-11-30T19:44:31Z",
  "total_results": 59,
  "confidence_score": "High",
  "data_quality": "Validated",
  "scope": "Corporate+DMZ endpoints only",
  "summary": "Brief description of findings",
  "risk_distribution": {...},
  "validation_notes": "Cross-checked with alternative query method"
}
```

## Error Recovery

### Common Clarifications
- Identifier type: hostname, IP address, MAC address, or device ID?
- Search scope: devices, vulnerabilities, or activities?
- Time frame: default 7 days for security, 30 days for vulnerabilities
- Asset scope: endpoints only, network devices, or all assets?
- Boundary context: Corporate, DMZ, or both?

### Validation Checks
- Cross-check query results when discrepancies detected
- Validate device counts across multiple query methods
- Confirm vendor name variations in security software detection

## Integration with OpenCode

### Tool Permissions
- **Armis MCP**: Full access for security operations
- **Write**: Ask permission for file modifications
- **Webfetch**: Ask permission for external documentation lookup
- **Read**: Full access for file analysis

### Agent Mode
- **Primary Agent**: Armis Query Agent for main security operations
- **Subagent Support**: SOC Analyst for specialized tasks
- **Context Management**: Commands maintain primary session context

## Development Guidelines

### Adding New Commands
1. Create markdown file in `.opencode/command/`
2. Set `agent: armis-query-agent` for consistency
3. Set `subtask: false` to maintain context
4. Follow the established error recovery patterns
5. Include scope clarification in command workflow

### Agent Modifications
1. Maintain temperature 0.1 for security analysis
2. Use permissions model for sensitive operations
3. Include validation framework in query construction
4. Follow confidence scoring guidelines
5. Document new capabilities in this AGENTS.md file

## Testing and Validation

### Recommended Test Scenarios
1. **Unprotected endpoint search** - Verify network device exclusion
2. **Critical vulnerability analysis** - Test risk prioritization
3. **Device lookup by hostname** - Validate multi-field search
4. **Security software inventory** - Test vendor name variations
5. **Large result sets** - Verify file output formatting

### Quality Assurance
- Cross-check query results with alternative methods
- Validate confidence scoring accuracy
- Test error recovery with ambiguous inputs
- Verify file output format consistency
- Confirm permission model effectiveness

## External Dependencies

### MCP Integration
- **Armis Security Remote MCP**: Primary data source for security operations
- **Tool Naming**: Uses `armis-security-remote-mcp_*` pattern for wildcard permissions

### Documentation References
- OpenCode Tools Documentation: https://opencode.ai/docs/tools/
- OpenCode Agents Documentation: https://opencode.ai/docs/agents/
- OpenCode Commands Documentation: https://opencode.ai/docs/commands/

## Additional Documentation

### Detailed Implementation Documents
- **[ARMIS_AGENT_IMPROVEMENTS_SUMMARY.md](./ARMIS_AGENT_IMPROVEMENTS_SUMMARY.md)** - Comprehensive enhancement details with problem areas addressed and impact analysis
- **[COMMAND_IMPLEMENTATION.md](./COMMAND_IMPLEMENTATION.md)** - Technical implementation details for all search commands
- **[OPENCODE_COMPLIANCE_REPORT.md](./OPENCODE_COMPLIANCE_REPORT.md)** - Full compliance validation against OpenCode best practices
- **[UPDATE_SUMMARY.md](./UPDATE_SUMMARY.md)** - Configuration updates and smart output handling implementation

### Key Features Summary
- **Smart Query Templates** - Optimized ASQ queries for common security patterns
- **Confidence Scoring** - Result reliability indicators (High/Medium/Low)
- **Result Validation** - Cross-check queries for consistency
- **Scope Clarification** - Automatic endpoint vs network device distinction
- **Error Recovery** - Comprehensive ambiguity resolution system

## Version History

### v2.0 (2025-11-30)
- Enhanced with OpenCode best practices
- Added temperature and permission configuration
- Improved error recovery and validation framework
- Added confidence scoring and data quality indicators
- Integrated smart query templates
- Enhanced file output format with metadata
- Full compliance validation documented
- Comprehensive command implementation

### v1.0 (Initial)
- Basic Armis query agent functionality
- Simple command structure
- Core ASQ translation capabilities