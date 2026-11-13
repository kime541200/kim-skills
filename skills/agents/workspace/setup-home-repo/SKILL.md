---
name: setup-home-repo
description: Turn a directory of sibling repos into a Home Repo, the agent launch base holding shared skills, docs and pointers to the others. Use when the user wants to set up, migrate to, or repair a multi-repo agent workspace.
disable-model-invocation: true
---

A **Home Repo** is one git repo that is the agent's launch base across several independent repos. It holds shared skills, root `AGENTS.md`, cross-repo docs and **pointers** to the other repos. The other repos stay independent, ignored by the Home Repo's `.gitignore`: never submodules, so a commit inside a child never dirties the Home Repo.

Child repos are never edited unless a step says so. Pushing and repo creation need explicit user confirmation.

## 1. Survey

Read the workspace root and each child: `git remote -v`, `AGENTS.md`/`CLAUDE.md`, `.gitignore`, `.agents/`, `skills-lock.json`, `docs/`. Check whether the root is already a git repo and what it ignores.

Done when you can state, per child: remote URL, role, whether it holds its own `AGENTS.md`, and whether it carries skills (generic duplicates of the root's, or project-specific).

## 2. Confirm the plan

Present the survey and the planned changes (steps 3-6). Ask only what the survey cannot settle: GitHub owner, root repo name, child roles when unclear, visibility (default `--private`). Wait for the answers.

## 3. Root `.gitignore` and clone script

- `.gitignore` lists every child directory plus `.env`, `tmp/`, `.scratch/`. Confirm `.env` is ignored before step 6's `git add .`.
- Add `scripts/clone-all.sh` from [templates/clone-all.sh](templates/clone-all.sh), filling `OWNER` and the repo list. Make it executable.

Done when `git status` (after step 6's `git init`) shows no child directory.

## 4. Root `AGENTS.md`

Write from [templates/AGENTS.md](templates/AGENTS.md). Keep it a router: the child table, on-demand clone, rule precedence, task routes, links to docs. Before writing, load `writing-for-agents` if available; then prune every line that restates what a child's own `AGENTS.md` or the environment already says.

Done when each child appears once with its role and full GitHub URL, and every pointer names its trigger condition.

## 5. Shared docs and skills

- Create `GLOSSARY.md` with only terms shared across children, and `docs/adr/0001-home-repo-architecture.md` recording the Home Repo and `.gitignore`-over-submodule decision. Use the `domain-modeling` skill's formats if available.
- Skills live once, in the root `.agents/skills/`. Children keep only project-specific skills. For each generic duplicate found in step 1, list it and ask the user before deleting it; then remove the child's copy and matching `skills-lock.json`.
- Make sure each child's `.gitignore` excludes generic `.agents/skills` and `skills-lock.json` yet leaves project-specific skills tracked, using negation rules, e.g. `.agents/skills/*` then `!.agents/skills/<project-skill>/`. List any `.gitignore` edit to the user before making it.

Done when every skill exists in exactly one place and no child `.gitignore` hides a project-specific skill.

## 6. Publish

1. `git init` the root and `git add .`.
2. Show `git status -s` to the user and wait for confirmation of the file list.
3. Commit, then `gh repo create <owner>/<name> --private --source=. --remote=origin --push`.

Done when the remote shows the commit and the report below is given.

## 7. Report

State: the repo URL, what the Home Repo tracks, the new-machine restore sequence (`gh repo clone`, then `./scripts/clone-all.sh`), and any child edits awaiting the user's decision.
