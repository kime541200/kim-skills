---
name: ambitious-framing
description: Reframe tasks across altitude, depth, and breadth using Minerva Habits of Mind before execution.
disable-model-invocation: true
---

# Ambitious Framing

Upgrade a request from a baseline **speed** task (doing the same work faster) across three ambition dimensions—**altitude**, **depth**, and **breadth**—anchored by explicit Minerva Habits of Mind and Foundational Concepts (`#hc` tags).

## 1. Classify the baseline and select HC lenses

Identify the literal deliverable requested and the task branch:

- **Analytical & Diagnostic**: root-cause analysis, research, data interpretation, or strategy evaluation.
- **Creative & Systems Design**: architecture, product/workflow design, or greenfield problem solving.
- **Decision & Communication**: executive synthesis, proposals, reviews, or stakeholder alignment.

Read [references/minerva-hcs.md](references/minerva-hcs.md) for the matching branch and select the active `#hc` tags that govern this task.

Done when the baseline deliverable, task branch, and active `#hc` tags are explicitly named.

## 2. Elevate altitude (`#rightproblem`, `#thesis`)

Step up one level of abstraction from the requested artifact to the decision or systemic outcome it serves:

- **Target the outcome (`#rightproblem`)**: reframe "produce document/patch X" into the concrete decision to unlock, the failure class to eliminate, or the system invariant to maintain.
- **Sharpen the thesis (`#thesis`)**: state the core decision at stake, the competing options, and what evidence would flip the choice.

Done when the goal is stated as a verifiable decision or system outcome rather than a surface deliverable.

## 3. Deepen to expert grounding (`#infoneeded`, `#sourcequality`, `#plausibility`, `#estimation`, `#correlation`, `#testability`)

Enforce domain-expert rigor before generating solutions:

- **Audit raw inputs (`#infoneeded`, `#sourcequality`)**: inspect primary sources (raw data, code, logs, traces, original specs) directly rather than building on summaries or unverified premises. List any missing raw inputs that live outside the workspace.
- **Apply expert methodology (`#plausibility`, `#estimation`, `#correlation`)**: name the methodology a top practitioner in the domain uses, test whether the problem's premises hold, and separate correlation from causation.
- **Fix an external rubric (`#testability`)**: define how the result will be verified outside self-assessment—via a deterministic check, a falsifiable prediction, or an explicit grading rubric.

Done when primary sources in the workspace are inspected, missing external inputs are inventoried, the domain methodology is named, and a falsifiable verification rubric is set.

## 4. Expand breadth (`#conformity`, `#diversity`, `#ethicalconflicts`)

Break single-domain tunnel vision by assembling a 2–3 lens crew across distinct disciplines (turn domain nouns into active verbs):

- **Cross-pollinate (`#diversity`)**: pair the primary domain specialist with an orthogonal discipline (for example, systems engineering × behavioral economics × visual communication).
- **Run an adversarial pass (`#conformity`)**: adopt a dedicated critic lens (such as a short-seller, incident postmortem lead, or skeptical user) tasked with finding how the framing or solution fails in practice.
- **Resolve trade-offs (`#ethicalconflicts`)**: reconcile competing constraints explicitly rather than averaging them into generic advice.

Done when at least two distinct disciplinary lenses and one adversarial critique have been applied and distilled into concrete adjustments.

## 5. Gate before speaking, then execute

Apply the pre-execution gate before producing the final artifact:

- **Hold on missing ground**: if Step 3 uncovered missing raw inputs (`#infoneeded`) that only the user can supply, or Step 2's altitude shift changes the authorized scope, present the **Ambitious Frame** (Elevated Outcome, Active `#hc` Checks, Missing Raw Inputs, and Proposed Plan) and wait for the user's answer.
- **Execute at full ambition**: when raw inputs and scope are sufficient, execute the upgraded task directly. Tag key reasoning checkpoints with their `#hc` tags and verify the final deliverable against Step 3's `#testability` rubric.

Done when either a sharp pre-execution gate is presented for missing inputs/scope, or the completed work satisfies the elevated outcome and passes the `#testability` rubric.
