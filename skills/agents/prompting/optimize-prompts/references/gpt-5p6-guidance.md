# GPT-5.6-specific prompt guidance

Source: [OpenAI, Prompting guidance for GPT-5.6 Sol](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6), reviewed 2026-07-16.

## Prompt controls

- GPT-5.6 is concise by default. Retain broad brevity instructions only when representative evals show they remain necessary.
- When available, use API `text.verbosity` for the default detail level and keep task-specific length and required content in the prompt.

## Programmatic Tool Calling

After code-driven orchestration passes the gate in `agentic-prompts.md`, use Programmatic Tool Calling only when the active GPT-5.6 runtime supports it.

Test both the `program_output` item and final assistant message because required fields or evidence can be lost between them.

## State and caching

- Preserve assistant phase values when manually replaying history. When supported, `previous_response_id` preserves prior assistant state automatically.
- Compact after major milestones, keep the functional prompt contract stable, and treat compacted items as opaque state.
- Reuse persisted reasoning while the objective, assumptions, and priorities remain stable. Use current-turn behavior after they change.
- Keep reusable prompt prefixes stable. Add explicit cache breakpoints only when measured cache behavior and cost improve.

## Reasoning effort

- Establish a baseline before changing reasoning effort. During migration from GPT-5.5 or GPT-5.4, preserve the current setting first and compare the same setting with one level lower.
- Use low for latency-sensitive work when quality holds, medium as a balanced starting point, high or xhigh when evals show a meaningful gain, and max for the hardest quality-first workloads.
- Before raising reasoning effort, check for a missing success criterion, dependency rule, tool route, or verification loop.

## Visual inputs

- Use original image detail for large, dense, OCR-heavy, or coordinate-sensitive images when the additional token cost and latency are justified.
- For incremental frontend work, provide product context and preserve the existing design system, responsive behavior, and required states. Render and inspect before finalizing.
