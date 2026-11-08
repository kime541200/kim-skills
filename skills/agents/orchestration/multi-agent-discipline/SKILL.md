---
name: multi-agent-discipline
description: Gate multi-agent delegation and enforce subagent role separation, structured handoffs, and layered verification. Use when deciding whether to spawn subagents or stay single-agent; designing or executing a multi-agent workflow; packaging context for a subagent handoff; splitting verification between deterministic checks and LLM evaluators; or auditing an agent pipeline for unnecessary complexity, token cost, or retry loops.
disable-model-invocation: false
---

# Multi-Agent Discipline

Default to a **single agent**. Over 60% of tasks execute faster, cheaper, and more reliably in one context window without coordination tax or cross-agent error amplification. Spawn multiple agents only when the task passes the necessity gate, and enforce strict role, handoff, and verification discipline when it does.

## 1. Apply the multi-agent necessity gate

Stay in a single agent unless at least one of these three conditions holds:

1. **Parallel execution**: the task decomposes into independent subtasks with disjoint scopes (files, modules, or data sources) that run concurrently to reduce wall-clock time.
2. **Cross-domain isolation**: the workflow requires incompatible instructions, tool permissions, or domain personas that would pollute or conflict inside a single context window.
3. **Adversarial validation**: the deliverable requires an independent critic or evaluator in a fresh context window to challenge the generator's output without self-confirmation bias.

Complete this step when the active gate (`parallel`, `isolation`, or `adversarial`) is explicitly identified with its concrete justification, or a **single-agent verdict** is reached and execution continues inline.

## 2. Isolate single-responsibility roles

When the necessity gate passes, assign each agent a single bounded responsibility:

- Separate **generation**, **execution/testing**, and **adversarial review** into distinct roles rather than asking one subagent to build and grade its own work.
- Define each role's exact input boundary, permitted tools, editable paths (or read-only constraint), and stop condition.
- Remove any proposed agent whose removal does not degrade task completion, accuracy, or wall-clock speed on representative test cases.

Complete this step when every agent role has one non-overlapping job, explicit tool/path boundaries, and a finite stop condition.

## 3. Package a structured handoff

Pass a compact **structured handoff packet** to each downstream agent instead of forwarding raw conversation history:

- **Objective**: the single task outcome required from this agent.
- **Scoped inputs**: only the extracted facts, file paths, schemas, and constraints needed for this role.
- **Output contract**: a fixed schema (such as JSON fields or a strict Markdown template) containing the task result, evidence citations, and unresolved blockers.

Complete this step when every subagent prompt carries a self-contained structured packet and omits unrelated conversational history.

## 4. Layer verification: mechanical first, LLM second

Split verification into two ordered tiers so an LLM never judges what deterministic code can prove:

1. **Mechanical gate (Deterministic)**: validate schema compliance, required fields, syntax, typechecks, linter rules, test suites, file existence, and numeric bounds using scripts, compilers, or CLI tools. Reject or repair outputs that fail the mechanical gate before invoking any evaluator model.
2. **Semantic gate (LLM Evaluator)**: use an adversarial LLM judge only after the mechanical gate passes, strictly for open-ended criteria that code cannot check (argument coherence, domain nuance, tone, or design trade-offs) against an explicit rubric.

Complete this step when every deterministic invariant is checked by code or CLI tooling, and any LLM evaluation is restricted to semantic rubric criteria after mechanical checks pass.
