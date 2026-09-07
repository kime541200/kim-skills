---
name: git-report
description: 從 Git commits 產生白話進度報告。使用者要求以 Git 紀錄整理週報、特定期間或 revision 範圍的工作摘要時使用；需要技術細節或工程日誌時採 engineer 受眾。
disable-model-invocation: false
---

# Git Report

## 1. Resolve the request and commit scope

Apply these defaults unless the user specifies otherwise:

- Repository: the current Git root.
- Revision: commits reachable from the current `HEAD`; include other refs only when requested.
- Author: all authors; filter only when requested.
- Audience: `manager`; use `engineer` for technical detail, maintainer context, or an engineering log.
- Format: `precise`; use `short` for a brief or one-line request and `full` for a complete or detailed request.
- Language: Traditional Chinese.
- Time: the current calendar week, from Monday 00:00 to now in the local timezone.

Use an explicit single commit, latest commit, commit count, revision range, or date range in place of the default time scope. Resolve relative dates into concrete local-time boundaries with an inclusive start and exclusive end. Derive a scope label such as `本週`, `上月`, `2026-07-01 至 2026-07-15`, or a revision name for the report heading.

Treat merge commits as grouping context when their child commits are already in scope. Count a merge separately only when it contains a unique change, so the same work appears once.

Completion criterion: the repository root, revision selector, author filter, time or revision scope, scope label, audience, format, and language form one unambiguous commit query before evidence gathering begins.

## 2. Load one audience format

- `manager`: read [`formats/manager.md`](formats/manager.md).
- `engineer`: read [`formats/engineer.md`](formats/engineer.md).

Apply the shared audience rules in that file and use the selected `precise`, `short`, or `full` section as the sole output schema.

Completion criterion: one audience file and one format section are selected; their shared rules and quality gates define the report.

## 3. Enumerate the commit set

Run `git log` with the resolved repository, revision, author, and range. Capture commit hashes for internal traceability, plus author date, subject, body, and parents. Record the exact selector or command used.

Fail distinctly when the repository or Git query is invalid. When the query succeeds with no commits, report that the resolved scope contains no commits and stop without inventing topics.

Create a commit ledger with one row per returned commit and an initial `unclassified` status.

Completion criterion: the Git query succeeds, every returned commit appears exactly once in the ledger, and the ledger represents the complete resolved scope.

## 4. Build the evidence ledger

Group related commits into candidate topics and map each topic to its commits. For every topic, record:

- What changed.
- Why or technical cause, when evidenced.
- User, delivery, maintenance, cost, or risk impact, when evidenced.
- Evidence level: subject/body, `git show --stat`, relevant diff, or an in-scope documentation change.

Inspect `git show --stat` for every nontrivial candidate topic. Read the relevant diff when the body and stat do not establish cause or impact, and for security, release, deployment, migration, compatibility, runtime, manifest, config, plugin entry, or CI claims that remain ambiguous. Use surrounding documentation only to explain an in-scope change, not to introduce unrelated work.

Assign every commit one final disposition: included in a topic, compressed into supporting work, omitted as low-signal noise, or used only as structural merge context.

Completion criterion: every nontrivial reported topic has evidence beyond its subject; every cause, impact, risk, blocker, or next-step claim points to evidence; and every commit has one documented disposition.

## 5. Rank and filter topics

Rank by impact rather than chronology:

1. Release, production, users, security, compliance, or external review.
2. Risk, cost, operational load, or accidental-failure reduction.
3. Product or technical capability.
4. Infrastructure, documentation, internal tools, or experience capture.

Merge repeated small commits into their topic. Compress typo fixes, repeated formatting, and mechanical cleanup unless they materially affect delivery, risk, or workflow. When impact is comparable, group by topic and use chronology only as a tie-breaker.

Completion criterion: every candidate topic is ranked or has an omission reason, and the highest-impact supported topic is first unless the selected audience format specifies a stronger grouping reason.

## 6. Write the report

- Ground every claim in the evidence ledger.
- Present grouped topics without commit hashes or filename-by-filename timelines.
- Explain what changed and the supported reason or impact.
- Include risks, blockers, and next steps only when evidenced by commits in scope.
- State low activity directly and stop after the supported topics.
- Use direct declarative phrasing; reserve `不是 A，而是 B` for correcting at most one likely misunderstanding.
- Rebuild the report from the evidence when changing audience instead of replacing terminology in place.

Completion criterion: the report follows the selected audience rules and sole format schema, uses the resolved scope label when the selected format includes one, and contains no empty or evidence-free section.

## 7. Verify before answering

Check that the commit set matches the recorded query, every reported topic maps to the ledger, the ordering follows the ranking, and every non-obvious claim has the recorded evidence. Apply the selected audience file's quality gates. Confirm that the output contains no internal hashes, raw file timeline, unsupported impact, or mixed format structure.

Completion criterion: every scope, evidence, ranking, audience, and format check passes; otherwise correct the report before answering.
