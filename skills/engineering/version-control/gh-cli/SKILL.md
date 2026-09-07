---
name: gh-cli
description: GitHub operations via `gh`. Use for cross-repository code search, Actions failure triage, Pages, pull requests, issues, releases, repository metadata, or an explicit request to use `gh`.
disable-model-invocation: false
---

# GitHub CLI

Use `gh` for GitHub-hosted state. Use local `git` for working trees, branches, commits, and diffs unless the task also involves GitHub state.

Resolve `<skill-dir>` as the directory containing this file. Invoke bundled scripts with absolute paths under `<skill-dir>`.

## Process

### 1. Resolve The Target

Resolve the repository and any run, PR, issue, release, branch, or filter named by the request. Use `gh repo view --json nameWithOwner,url` when the current repository is relevant, and use `gh auth status` when access or authentication is uncertain. Before a remote mutation, ask only when the intended action or target remains ambiguous.

Completion criterion: the repository and every identifier needed by the selected operation are unambiguous.

### 2. Select One Branch

Inspect only the selected script's `--help` or the relevant `gh <command> --help` before constructing non-trivial options.

| Branch | Route | Completion criterion |
| --- | --- | --- |
| Cross-repository code search | Run `<skill-dir>/scripts/gh_code_search.py`. | Report the query, filters, requested limit, returned count, and each actionable result with repository, path, URL, and relevance. |
| Actions failure triage | Run `<skill-dir>/scripts/gh_failed_run.py`; pass `--run-id` when the user identifies a run, otherwise triage the latest failed run. | Report the selected run ID and URL, failed jobs, first actionable evidence from each job, and either a confirmed cause or the next diagnostic hypothesis. Label excerpts as evidence rather than automatically treating them as root cause. |
| GitHub Pages | Run `<skill-dir>/scripts/gh_pages_deploy.py`. Inspect `status` before `enable` or `rebuild`. For `create-workflow`, choose the repository's actual artifact path; an existing workflow requires explicit overwrite authorization. | Report the repository, prior Pages state, authorized mutation or local file write, resulting state, and verification result. |
| General GitHub operation | Use the relevant `gh` subcommand and its help. | Report the repository, identifiers or filters, result, whether remote state changed, and post-mutation verification when applicable. |

### 3. Inspect, Act, And Verify

Prefer structured JSON output for inspection. Perform remote mutations only when the request authorizes the action and Step 1 resolved the target. Use non-interactive PR and issue commands by default; choose `--web` when the user requests a browser flow. Leave `gh alias` configuration unchanged unless alias management is the requested task.

After a mutation, query GitHub again when the resulting state is observable. Use the branch completion fields as internal checks; report the requested result, useful links, and material remaining uncertainty without listing irrelevant fields.

Completion criterion: every requested operation is accounted for, and every mutation is either verified or explicitly reported as unverifiable with the reason.
