---
name: to-devlog
description: Record why a session's changes were made as a project devlog.
disable-model-invocation: true
---

# To Devlog

Record **why** this session's changes were made as a project devlog. Git history is the source of truth for *what* changed; this note preserves the reasoning that diffs and commit subjects leave behind.

## 1. Inventory scope and rationale

Identify this session's changes—its commits and uncommitted work—or the commit range the user specifies. Use `git log --stat` (and `git status --short` for uncommitted work) alone to group changes by topic.

For each change group, collect its **grounded** rationale from the session (trigger, decisions, rejected alternatives, trade-offs, revisit triggers). Tag each group as **grounded** (explicitly established in this session) or **unexplained** (e.g., manual edits or commits whose motivation was never discussed).

Done when every in-scope commit and uncommitted change belongs to a topic group tagged **grounded** or **unexplained**.

## 2. Gate on ambiguity or missing rationale

Pause and ask the user before writing if either condition holds:

- The scope is ambiguous (for example, unrelated commits on the branch or uncommitted work that may or may not belong).
- Any change group is **unexplained**—list those items and ask the user for their motivation.

When scope and rationale are clear, proceed directly.

Done when scope is unambiguous and every included group is **grounded** (from the session or the user's reply).

## 3. Resolve destination and conventions

- Use the path the user specifies. Otherwise, check `docs/` for an existing devlog or decision-log directory (such as `docs/devlog/`, `docs/decisions/`, `docs/rationale/`) and follow its directory, naming, and structure conventions.
- Default when none exists: `docs/devlog/YYYY-MM-DD-<slug>.md` using a concise kebab-case topic slug. Create a folder `docs/devlog/YYYY-MM-DD-<slug>/README.md` only when accompanying artifacts (benchmarks, diagrams, logs, appendices) belong beside the note.
- Language: follow the user's conversation language unless neighbouring devlog files establish another language.

Done when the output path, single-file vs. folder layout, and language are fixed.

## 4. Write the why-first devlog

Organize by topic, keeping every claim **grounded** in session evidence and writing what a future reader cannot infer from `git log`. Follow existing neighbouring conventions when present, or use this default structure:

- **Title & Date**: topic title and date (`YYYY-MM-DD`).
- **Context & Problem**: what triggered the change and why now.
- **Decisions & Trade-offs**: each key choice, why it beat concrete alternatives, known trade-offs, and **revisit triggers** (conditions under which to reconsider).
- **Commits**: a compact list of short hashes and one-line summaries (reference paths only to anchor a decision). Note uncommitted scope explicitly when changes are not yet committed.
- **Follow-ups**: concrete remaining items or open questions; omit this section when none exist.

Done when the file is written, every included group is backed by **grounded** rationale, and each commit entry is limited to a short hash and one-line summary.

## 5. Report

State the created file path and the commits (or uncommitted scope) covered. Leave committing to the user after review; do not auto-commit.
