---
name: agy-delegate
description: Delegate a large corpus sweep to a low-cost Gemini model through the Antigravity CLI (`agy`) when the input is large, the work is mechanical and low-judgment, and only an evidence-backed digest needs to return to the current context. Use for repository-wide inventories, large logs or datasets, mechanical compliance sweeps, whole-repository summaries, or multi-page web research. Use native search for targeted lookups such as locating a symbol or file.
disable-model-invocation: false
---

# Delegate corpus sweeps to agy

## 1. Confirm the delegation fit

Proceed only when all three gates hold:

1. The corpus is large enough that reading it in the current context would be expensive.
2. The work is mechanical extraction, enumeration, or digestion rather than nuanced judgment.
3. The current context needs an evidence-backed digest rather than the source material itself.

Use native search or exploration for a targeted lookup. Complete this step when each gate has a concrete yes; otherwise continue with native tools.

## 2. Select the model

Run `agy models`, then select by this order:

1. The exact returned ID for the newest Gemini Flash model at the `high` tier.
2. If unavailable, use another returned model only when its known cost and capability fit the bounded mechanical task.
3. If no suitable model is established, continue with native tools; newest does not imply low cost.

Complete this step when the value passed to `--model` appears verbatim in the current `agy models` output.

## 3. Build a bounded prompt

Write a self-contained prompt that includes:

1. The working directory and exact paths, URLs, queries, or file patterns in scope.
2. A read-only boundary: inspect the named sources, return findings, and leave the workspace unchanged.
3. The exact extraction or digestion task.
4. The required output schema.
5. An evidence field for every finding, such as a file and line number or a source URL.
6. A coverage ledger for an inventory or sweep: inputs discovered, inputs checked, inputs skipped with reasons, errors, and result count.
7. A finite source, query, and date boundary for web research, where exhaustive coverage is not possible.

For an inventory, require `checked + explicitly skipped = discovered` with no unexplained gap. Complete this step when the prompt contains the scope, read-only boundary, task, output schema, evidence requirement, and applicable coverage boundary.

## 4. Run in a sandbox

```bash
agy -p "<prompt>" \
  --model "<exact model ID from agy models>" \
  --sandbox \
  --dangerously-skip-permissions \
  --print-timeout 15m
```

`--dangerously-skip-permissions` auto-approves tool permission requests. Use it only when the effective sandbox restrictions have been verified as appropriate for the authorized task; a read-only prompt is not filesystem enforcement. If adequate restrictions cannot be established, complete the sweep with native tools instead. Add one `--add-dir <path>` for each required directory outside the working directory. Ask for web research in the prompt; no separate web flag is required. Increase the timeout when the bounded corpus reasonably needs more than 15 minutes.

Complete this step when the process exits successfully and one complete digest has been captured. Treat a timeout, non-zero exit, or partial response as a failed run rather than a result.

## 5. Parallelize independent sweeps

For unrelated sweeps, start one tracked execution or session per job with the host's parallel mechanism. Keep their outputs separate and wait for every job to finish.

Complete this step when every job has exited successfully and every digest has been captured; surface each failed job explicitly.

## 6. Verify before use

Treat the delegated digest as provisional evidence:

- Before an edit or decision, verify every claim that drives that action against its cited source.
- For a non-actionable summary, verify the coverage ledger and at least one finding from every output category or source type.

Complete the delegation when the applicable checks pass. If a check fails, correct the scope or prompt and rerun the sweep, or finish the affected portion with native analysis.
