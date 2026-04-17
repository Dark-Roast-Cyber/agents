---
description: General Armis security query with smart output handling
agent: armis-query-agent
subtask: false
---
Identify the security query intent from: $ARGUMENTS
Then construct and execute a valid Armis ASQ query to answer the request.

The agent will automatically:
- Display results directly if ≤ 20 items
- Write full results to file if > 20 items
- Always provide clear output location and summary
- Use structured JSON format for file outputs
