---
name: optimize-prompts
description: Optimize prompt artifacts. Use for explicit prompt audits, rewrites, or migrations; reusable system or developer prompts, agent instructions, prompt templates, or tool descriptions with observable defects likely to reduce correctness or precision; reported prompt-specific failures or regressions; and tasks materially blocked by prompt ambiguity, conflicting rules, weak grounding, missing completion or permission boundaries, or faulty tool routing. Treat direct task requests as execution requests unless the text is framed for reuse or another model/runtime.
disable-model-invocation: false
---

# Optimize Prompts

Build the shortest complete prompt contract. Diagnose before editing, preserve intent, and require every change to repair an observable defect.

## Steps

### 1. Classify the text and scope the target

- Classify the text as an explicit optimization request, a reusable prompt artifact, or a direct execution request.
- For an explicit request, follow the requested branch: audit only, rewrite, or model migration.
- For a reusable prompt artifact, invoke implicitly only when an observable defect is likely to materially affect correctness, precision, grounding, authority, tool use, or completion. Use rewrite unless the context calls for audit or migration.
- For a direct execution request, complete the task directly. Enter prompt optimization only when a prompt defect materially blocks completion.
- Ask one focused question when artifact versus execution intent cannot be inferred and would change the action taken.
- Identify the target model/runtime when known, the artifact, and editable instruction layers.
- Treat supplied higher-priority and non-editable layers as constraints. Limit claims to supplied or inspectable layers.
- Use model-agnostic guidance unless a verified target-specific behavior matters. Ask about the model only when it would materially change the result.

Complete this step when the text's role, authorized outcome, model class, branch, editable boundary, and immutable constraints are confirmed or represented by a narrow stated assumption.

### 2. Apply the necessity gate

Proceed only when at least one observable defect exists:

- materially ambiguous outcome or audience;
- conflicting, duplicated, or obsolete instructions;
- missing input, evidence, or context whose absence changes the result;
- missing success criteria, validation, or finite stop conditions for a non-trivial task;
- unclear autonomy, side-effect, approval, or scope boundaries;
- faulty tool, retrieval, citation, retry, or fallback routing;
- unverifiable output requirements;
- a regression demonstrated by representative traces or evals.

When no defect exists, return a no-change verdict, preserve the original prompt, and offer at most one optional refinement.

Complete this step when every claimed defect is tied to supplied wording or a concrete omission, or a no-change verdict has been reached.

### 3. Recover the prompt contract

- State the intended user-visible outcome in one sentence.
- Record explicit values, facts, language, format, audience, constraints, evidence requirements, and permission boundaries.
- Separate invariants from judgment calls; express judgment calls as decision rules.
- Resolve contradictions using runtime instruction precedence and the user's stated intent.
- Ask for the smallest missing fact only when different answers would materially change the result or authorized actions. Otherwise record the narrow assumption used.
- Source every added value from the user or supplied context. Represent unresolved material choices—such as audience, geography, time range, or target runtime—with one focused question or a labeled placeholder.

Complete this step when the outcome, invariants, decision rules, required output, permissions, and material assumptions are explicit enough to validate preservation, and every added value is sourced or visibly unresolved.

### 4. Choose the execution mode

Optimize directly when the artifact is short, single-layer, tightly coupled to the current conversation, or cheaper to handle than to hand off and verify.

Delegate a bounded audit or rewrite to a subagent when at least one applies:

- the prompt stack is long or spans multiple instruction layers;
- several artifacts or variants require the same analysis;
- migration requires comparing substantial traces or eval results;
- the task contains a large mechanical diagnosis or rewriting stage;
- an independent pass would materially improve confidence.

When delegating:

- select the lowest-cost available model with sufficient reasoning quality, context capacity, language ability, and runtime access;
- select by required capability rather than a hard-coded model name;
- pass the raw artifact, intended outcome, target model/runtime, editable layers, preservation requirements, and requested branch;
- require every proposed edit to map to an observable defect;
- have the primary agent validate preservation, instruction precedence, unsupported additions, and the final response contract;
- continue directly when suitable model selection or subagent execution is unavailable.

Complete this step when the execution mode minimizes expected total cost, including handoff and verification, without lowering the required confidence.

### 5. Execute the selected branch

Before evaluating or editing tool-using agents, grounded research, long-running work, approval-sensitive actions, or multi-stage validation, read [references/agentic-prompts.md](references/agentic-prompts.md).

For model-specific changes, consult current official guidance for the exact target model and active runtime. For a GPT-5.6-family target, [references/gpt-5p6-guidance.md](references/gpt-5p6-guidance.md) is a scoped reference; do not apply its defaults to other models. Keep legacy references scoped to their original models.

- **Audit only:** cite defects and recommend the smallest effective corrections. Keep the supplied artifact intact.
- **Rewrite:** remove obsolete, duplicated, inert, and irrelevant content before adding rules. Put the outcome, success criteria, hard constraints, required output, and stop rules ahead of optional process detail. Preserve explicit claims, values, genre, length, and structure unless the user requests otherwise. Keep unresolved material choices as labeled placeholders.
- **Model migration:** establish a baseline on representative cases, change one prompt or runtime variable at a time, rerun the same cases, and retain only changes supported by the comparison.

Complete this step when every audit finding maps to supplied wording or a concrete omission, every rewrite edit maps to a diagnosed defect and preserves the recovered contract, or every retained migration change has an attributable eval result.

### 6. Validate the result

- Compare the result against the recovered prompt contract and diagnosed defects.
- Confirm that all explicit user values are preserved, the instructions are internally consistent, and required output and completion are observable.
- Confirm that every added rule is necessary and that relevant approval, evidence, fallback, retry, and stop behavior passes the selected agentic or model-specific guidance.
- Apply the same checks to delegated candidates; delegation changes who performs the work, not the completion bar.
- Prefer correctness and completion over token count, latency, or stylistic polish.

Complete this step when every diagnosed defect is resolved or explicitly left open, every explicit value is preserved, and the selected branch's output contract passes.

## Response contract

Follow the user's requested output shape. Otherwise return:

- **No change:** `Verdict`, reason, and at most one optional refinement.
- **Audit only:** `Verdict`, `Findings`, and `Recommended changes`.
- **Rewrite:** `Verdict`, `Findings`, `Optimized prompt`, and `What changed`.
- **Model migration:** the rewrite fields plus `Eval comparison`.
- Include assumptions only when they materially affect confidence.

If the user requests only the rewritten prompt, return only that prompt.
