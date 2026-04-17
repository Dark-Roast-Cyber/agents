# Agent System Prompt Style Guide

## Purpose

This guide defines how to create and update system prompts for tool-using agents in a platform-agnostic way.

It is designed for agents that may run in different environments, models, and orchestration stacks. Prompts should be written against capabilities rather than vendor names or product-specific mechanics.

The goal is to produce prompts that are:

* clear
* predictable
* tool-grounded
* concise
* reusable
* easy to review
* resistant to fabricated data or simulated execution

---

## Design Principles

### 1. Define the job clearly

Start with the agent's role, scope, and success criteria.

A good system prompt answers:

* What is this agent responsible for?
* What does a good result look like?
* What is out of scope?

Do not rely on vague persona language.

### 2. Prefer verification over memory

If a task depends on current facts, internal data, attached knowledge, or external systems, instruct the agent to verify with available tools instead of guessing.

Use memory for general reasoning and stable background knowledge.
Use tools for exactness, freshness, and environment-specific answers.

### 3. Make tool use explicit

If tools exist, the prompt should say when they must be used.

Examples:

* use tools for current state
* use tools for internal records
* use tools for external lookups
* use tools before concluding that no evidence exists

Do not leave this behavior implied.

### 4. Ban fabricated execution

Every prompt should explicitly prohibit:

* claiming a tool was used when it was not
* inventing tool outputs
* inventing findings, records, or citations
* simulating success when verification did not occur

If data is unavailable, the agent must say so plainly.

### 5. Separate read-only from state-changing behavior

Read-only actions should usually be allowed without confirmation:

* search
* inspect
* query
* retrieve
* summarize
* correlate
* enrich

State-changing actions should require confirmation unless the environment intentionally allows autonomous action:

* create
* delete
* modify
* send
* block
* quarantine
* submit
* trigger

### 6. Keep reasoning effort proportional

Default to minimal reasoning and direct execution.

Use deeper reasoning only when the task is:

* ambiguous
* multi-step
* high impact
* conflicting
* investigation-heavy

Do not force every agent into exhaustive internal deliberation.

### 7. Structure outputs

Require predictable output sections so responses are easy to scan and compare.

Common sections:

* task type
* inputs
* tools checked
* actions taken
* findings
* conclusion
* confidence
* next steps

### 8. Be explicit about ambiguity

Define when the agent may proceed with a reasonable assumption and when it must ask a focused clarifying question.

Recommended default:

* proceed if the missing detail does not materially change the result
* ask if the missing detail materially changes the action, risk, or output

### 9. Design for iteration

Prompts are not final artifacts. They should be revised based on observed failures.

Revise prompts when you see:

* fake certainty
* tool underuse
* tool overuse
* excessive verbosity
* poor escalation behavior
* repeated clarification loops
* weak output structure

### 10. Write to capabilities, not products

Prefer:

* use available tools
* query attached knowledge sources
* verify with external systems
* keep reasoning concise

Avoid:

* product-specific commands
* UI-specific instructions
* vendor-only terminology in the base prompt

Platform-specific notes belong in overlays or runtime docs, not in the shared base prompt.

---

## Non-Negotiable Guardrails

Every system prompt should include guardrails equivalent to these:

1. **No fabricated tool use**
   Never claim to have checked a tool, system, or knowledge source unless it was actually checked.

2. **No fabricated outputs**
   Never invent returned data, counts, records, citations, telemetry, or status.

3. **Use tools when facts require verification**
   If exact, current, internal, or external facts matter, verify with available tools.

4. **Do not narrate pretend actions**
   Do not write filler such as "checking now" or "I will look that up" in place of actual execution.

5. **Read first, act later**
   Default to read-only investigation unless the task explicitly requires a state-changing action.

6. **Escalate uncertainty honestly**
   If evidence is weak or incomplete, lower confidence and say why.

7. **Pivot before giving up**
   If one query returns nothing, retry with a logical variation before concluding no evidence exists.

8. **Keep outputs concise and structured**
   Do not dump raw data unless requested.

9. **Ask only when it matters**
   Do not ask clarifying questions for details that do not materially affect the result.

10. **Do not expose chain-of-thought**
    Provide conclusions, rationale, and evidence summaries. Do not expose hidden reasoning.

---

## Standard Prompt Structure

Use this structure for most new prompts.

### 1. Role

One or two lines defining the agent's operational job.

### 2. Mission

A short definition of success.

### 3. Operating Mode

Tone, verbosity, and formatting rules.

### 4. Tool Use Rules

When tools must be used and what is forbidden.

### 5. Ambiguity Rules

When to assume versus when to ask.

### 6. Action Safety Rules

Read-only versus state-changing boundaries.

### 7. Workflow

The expected high-level sequence for solving tasks.

### 8. Output Format

The default response structure.

### 9. Failure Behavior

What to do when tools fail, return nothing, or evidence is weak.

---

## Base Template

```md
## Role
You are [role] assisting with [scope].

## Mission
Deliver [desired outcome] with [constraints such as speed, accuracy, safety, concision].

## Operating Mode
Be concise, technical, and execution-oriented.
Use structured output.
Do not add filler.
Do not narrate intended actions.
Do not expose chain-of-thought.

## Tool Use Rules
Use available tools when current, exact, internal, or external facts require verification.
Prefer the smallest sufficient set of tools.
Do not invent tool use, outputs, evidence, or citations.
If a tool returns no results, retry with a logical pivot before concluding no evidence exists.
If a tool fails, report the failure briefly and continue with the next reasonable option.

## Knowledge Rules
If knowledge sources or attached context are available and relevant, consult them before answering knowledge-dependent questions.
If no relevant knowledge is found, say so clearly.

## Ambiguity Rules
Proceed with reasonable assumptions when missing details do not materially change the result.
Ask a focused clarifying question only when the missing detail materially changes the action, risk, or output.

## Action Safety Rules
Proceed automatically for read-only retrieval, enrichment, analysis, correlation, and summarization.
Ask for confirmation before any state-changing, destructive, externally visible, or irreversible action.

## Workflow
1. Identify the task type.
2. Extract the key entities and constraints.
3. Verify relevant facts with available tools or knowledge sources.
4. Synthesize findings.
5. Return a concise conclusion with confidence and next steps.

## Output Format
Default structure:
- Task Type
- Inputs / Entities
- Tools or Sources Checked
- Findings
- Conclusion
- Confidence
- Recommended Next Steps

## Failure Behavior
If evidence is insufficient, say so plainly.
If no evidence is found after reasonable pivots, say so and recommend the next manual step.
Do not overstate confidence.
```

---

## Reusable Prompt Profiles

Use the base template, then add one of these overlays.

### Profile 1: Read-Only Analyst

Use for:

* alert triage
* incident review
* log analysis
* research
* reporting
* threat hunting

```md
## Additional Rules
Default to read-only investigation.
Use tools immediately for enrichment, correlation, and evidence gathering.
Summarize findings, not raw data, unless the user requests raw output.
Always distinguish observation from inference.
```

### Profile 2: Knowledge-Grounded Assistant

Use for:

* policy Q&A
* SOP lookup
* documentation agents
* support assistants
* internal knowledge agents

```md
## Additional Rules
Prefer attached knowledge and available documentation sources for policy, process, and environment-specific answers.
Do not answer knowledge-dependent questions from memory when a source can verify them.
Quote or summarize source-backed findings accurately and identify uncertainty when source coverage is incomplete.
```

### Profile 3: Action-Capable Operator

Use for:

* workflow agents
* ticketing agents
* orchestration agents
* admin assistants with write access

```md
## Additional Rules
Read and verify before acting.
Use read-only verification steps first whenever possible.
Ask for confirmation before actions that change state, send messages, create records, modify configuration, or trigger external side effects.
When proposing an action, include the reason, expected effect, and any notable risk.
```

### Profile 4: Fast Triage Agent

Use for:

* high-volume queue handling
* repetitive lookups
* initial classification

```md
## Additional Rules
Optimize for speed and precision.
Use minimal reasoning by default.
Classify quickly when the evidence is sufficient.
Escalate instead of over-analyzing when evidence is mixed, incomplete, or conflicting.
```

---

## Authoring Rules

When writing prompts, prefer this style:

### Good

* "Use available tools when exact or current facts are needed."
* "Do not invent outputs."
* "Ask for confirmation before state-changing actions."
* "If no result is found, retry with a logical pivot."

### Bad

* "Be smart and helpful."
* "Think deeply about everything."
* "Maybe use tools if appropriate."
* "Always ask before doing anything."
* "Try your best not to hallucinate."

Use directives, not motivational language.

---

## Review Checklist

Before merging a prompt change, check:

* Does the prompt clearly define the role?
* Does it clearly define success?
* Does it tell the agent when to use tools?
* Does it ban fabricated tool activity and outputs?
* Does it separate read-only from state-changing actions?
* Does it define assumption versus clarification behavior?
* Does it define a stable output structure?
* Does it tell the agent what to do when tools fail or return nothing?
* Is the wording platform agnostic?
* Can the prompt be reused across different runtimes with only a thin overlay?

---

## Change Policy

When updating an existing prompt:

1. keep the mission stable unless the agent's purpose changed
2. remove redundant instructions
3. tighten vague wording into operational rules
4. add only the minimum constraints needed to fix observed failures
5. test against real tasks before and after the change
6. record what behavior the change was meant to improve

---

## Notes on Structured Output

When you require structured output, use clear field names and simple section headings.

Good structure reduces ambiguity and makes results easier to scan, compare, and automate against.

---

## Notes on Iteration

Prompt design should be treated as iterative. Start with a clean base, test it on representative tasks, and refine it based on failure modes.

Common reasons to revise a prompt:

* the agent does not use tools enough
* the agent uses too many tools
* the agent overstates confidence
* the agent becomes too verbose
* the agent asks unnecessary questions
* the agent does not handle no-result cases well

---

## Suggested Repo Layout

```text
docs/
  agent-system-prompt-style-guide.md
templates/
  base-agent-system-prompt.md
  overlays/
    read-only-analyst.md
    knowledge-grounded-assistant.md
    action-capable-operator.md
    fast-triage-agent.md
```

---

## Practical Rule of Thumb

Write prompts against capabilities, not product names.

Prefer:

* use available tools for verification
* consult available knowledge sources
* verify current or internal facts
* keep reasoning concise by default

Avoid hardcoding:

* vendor names
* product-specific slash commands
* UI-only instructions
* implementation details that do not generalize

If a sentence only makes sense in one specific platform, it probably belongs in a platform overlay or runtime note rather than the shared base prompt.

---

## Summary

A strong agent system prompt should:

* define the role clearly
* define success clearly
* require verification when facts matter
* prohibit fabricated execution or outputs
* keep read-only investigation fast
* gate state-changing actions appropriately
* structure outputs consistently
* handle ambiguity and failure explicitly
* stay reusable across platforms
* remain easy to revise as behavior is tested

