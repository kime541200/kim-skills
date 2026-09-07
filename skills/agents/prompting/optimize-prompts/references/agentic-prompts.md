# Model-agnostic agentic prompt guidance

## Agentic contract

Select only sections that change behavior:

```text
Role: [function and relevant context]
Goal: [user-visible outcome]
Success criteria: [observable completion bar]
Constraints: [safety, policy, evidence, permissions, scope]
Tools: [routing, prerequisites, fallbacks, relevant return fields]
Output: [required format, content, length, language]
Stop rules: [when to retry, ask, abstain, fall back, or finish]
```

Omit empty sections.

## Autonomy and approval

- Map request type to authority. Answer, explain, review, diagnose, and plan normally authorize inspection and reporting. Change, build, and fix normally authorize in-scope local edits and non-destructive validation.
- Infer authorization from the request and conversation. Ask when required authorization is missing, the target or effect is materially ambiguous, or the action exceeds the authorized scope; do not ask again for an already authorized action. Complete independent authorized preparation before pausing, and respect the host permission boundary.
- State the current work layer—research, design, implementation, review, or external coordination—when silently moving between layers would be risky.
- Keep each permission rule in one place so safe, expected actions do not trigger unnecessary pauses.

## Tools and retrieval

- Expose only task-relevant tools. Describe what each tool does, when to use it, important return fields, and relevant error behavior.
- Resolve prerequisite discovery, retrieval, and validation before acting.
- Parallelize independent reads. Keep dependent decisions sequential and synthesize parallel results before acting.
- For empty, partial, or suspiciously narrow results, use one or two meaningful fallbacks before concluding that evidence is absent.
- Use direct tool calls when one call is enough, each result changes the next decision, approval is involved, or native citations and artifacts must survive.
- Use code-driven orchestration for a bounded deterministic stage such as filtering, joining, ranking, deduplication, aggregation, batching, or repeated validation when the runtime supports it. Define eligible tools, compact output schema, retry limit, stop condition, and the handoff back to model judgment.

## Grounding and citations

- Define which claims require support and what counts as enough evidence. Treat missing evidence as unknown rather than proof of a negative.
- Cite only retrieved sources and attach citations to the claims they support. Separate inference from sourced fact and report source conflicts.
- Retrieve again for a missing required fact, owner, date, ID, source, exhaustive comparison, named artifact, or otherwise unsupported material claim.
- For creative drafts, keep source-backed facts distinct from creative wording. Preserve names, metrics, dates, status, outcomes, and capabilities exactly unless the source supports a change.

## Long-running work

- Request a short user-visible preamble before tools, then sparse outcome-based updates at major phase changes. Keep routine tool narration out of the prompt.
- Preserve the objective, assumptions, decisions, blockers, and next action across compaction or handoff using mechanisms the runtime actually provides.
- Define finite retry and fallback budgets.
- Recheck assumptions when new evidence changes the objective or priorities.

## Artifact-specific validation

- For code, choose checks proportionate to the change and complete repository-required checks. Add tests only when they independently verify meaningful behavior. After checks pass, broaden or repeat them only for new changes, failures, or unresolved concerns. State the next-best check when validation cannot run.
- For visual artifacts, require rendering and inspection of layout, clipping, spacing, missing content, and consistency.
- For plans, require named resources, state or data flow, validation, failure behavior, security or privacy considerations, and material open questions.
