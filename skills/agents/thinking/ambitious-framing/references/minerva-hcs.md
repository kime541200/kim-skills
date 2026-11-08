# Minerva Habits of Mind & Foundational Concepts (HCs)

Select only the `#hc` tags relevant to the active task branch. Use each tag as an explicit cognitive check, never as decorative label text.

## Branch 1: Analytical & Diagnostic (Critical Thinking — Claims, Evidence & Causality)

- `#assertions` — Separate explicit premises from conclusions; expose unstated assumptions holding an argument together.
- `#critique` — Interrogate claims for internal consistency, hidden leaps, and alternative explanations.
- `#infoneeded` — Specify the exact missing evidence required to confirm or refute a claim before acting.
- `#sourcequality` — Rank evidence by proximity to reality: raw data, reproducible code, and primary logs over secondary summaries or opinions.
- `#estimation` — Run back-of-the-envelope Fermi checks to test whether quantitative claims or scale assumptions are physically and economically plausible.
- `#plausibility` — Evaluate whether a hypothesis rests on sound mechanisms before investing in execution.
- `#testability` — Formulate hypotheses and success criteria so they yield observable, falsifiable predictions.
- `#epistemology` — Distinguish observed facts, operational definitions, testable hypotheses, and unfalsifiable opinions.
- `#scibreakdown` — Diagnose flaws in experimental or evaluation design (confounders, survivorship bias, cherry-picked baselines).
- `#probability` & `#conditionalprob` — Base judgments on base rates and conditional updates ($P(A|B)$ vs. $P(B|A)$) rather than narrative salience.
- `#sampling` — Check whether the observed cases represent the target population or suffer from selection bias.
- `#effectsize` & `#confidenceintervals` — Separate practical magnitude and uncertainty bounds from mere noise or point estimates.
- `#correlation` — Reject causal claims backed only by co-occurrence; require a mechanism, intervention, or natural experiment.
- `#regresstomean` — Account for extreme observations naturally moving toward the average on re-measurement before crediting an intervention.

## Branch 2: Creative & Systems Design (Thinking Creatively — Framing, Modeling & Iteration)

- `#rightproblem` — Frame the underlying root problem and desired system state rather than optimizing a symptom or surface request.
- `#constraints` — Inventory hard invariants versus negotiable preferences so design space is neither artificially narrowed nor ungrounded.
- `#divergent` — Generate structurally distinct options across different mechanisms before converging on a single design.
- `#analogies` — Transfer proven structural solutions from an unrelated discipline that shares the same underlying constraint topology.
- `#systemmodeling` — Map stocks, flows, feedback loops, and bottlenecks to predict second-order effects before modifying a component.
- `#emergence` — Anticipate system-level behaviors (race conditions, perverse incentives, cascading retries) that do not appear in isolated unit checks.
- `#prototyping` — Build the smallest falsifiable slice to retire the highest-risk assumption first.

## Branch 3: Decision & Communication (Communicating & Interacting Effectively)

- `#thesis` — Lead with a crisp, falsifiable recommendation or decision claim rather than a topic summary.
- `#audience` — Calibrate abstraction level, evidence density, and terminology to the decision-maker's context and action space.
- `#organization` — Structure arguments so the governing conclusion, supporting evidence, and counter-arguments are immediately navigable.
- `#composition` & `#connotation` — Choose precise terms with unambiguous operational meaning; strip hedging that obscures accountability.
- `#conformity` — Counteract groupthink and sycophancy by running a dedicated adversarial red-team pass against the preferred conclusion.
- `#diversity` — Combine non-overlapping disciplinary perspectives to expose blind spots no single specialist role catches.
- `#powerdynamics` & `#orgstructure` — Account for ownership boundaries, incentives, and operational handoffs that determine whether a technical solution survives in practice.
- `#ethicalframing` & `#ethicalconflicts` — Surface competing values or safety/speed trade-offs explicitly and state the context-specific priority rule used to resolve them.
- `#responsibility` — Define concrete ownership, verification gates, and rollback triggers rather than leaving execution open-ended.
