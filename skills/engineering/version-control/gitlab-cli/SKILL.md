---
name: gitlab-cli
description: GitLab operations via `glab`. Use for issues, merge requests, pipeline failure triage, releases, repository metadata, API calls, or exporting issues to Markdown.
disable-model-invocation: false
---

# GitLab CLI

Use `glab` for GitLab-hosted state. Use local `git` for working trees, branches, commits, and diffs unless the task also involves GitLab state.

Resolve `<skill-dir>` as the directory containing this file. Invoke bundled scripts with absolute paths under `<skill-dir>`.

## Process

### 1. Resolve The Target

Resolve the GitLab host, full project path, and any issue, merge request, pipeline, job, release, branch, or filter named by the request. Use explicit `-R group/subgroup/repo` or a full project URL for nested namespaces, ambiguous remotes, or a 404 caused by auto-detection. Use `glab auth status` when access or authentication is uncertain.

Keep TLS verification enabled. Change host TLS policy only when the user or repository policy explicitly authorizes the risk.

Completion criterion: the GitLab host, project, and every identifier needed by the selected operation are unambiguous.

### 2. Select One Branch

Inspect the relevant `glab <command> --help` or selected script's `--help` before constructing non-trivial options; `glab` flags vary by command and version.

| Branch | Route | Completion criterion |
| --- | --- | --- |
| Issues and merge requests | Use `glab issue ...` or `glab mr ...`. | Report the project, identifiers or filters, result summary, whether remote state changed, and post-mutation verification when applicable. |
| Pipeline failure triage | Use `glab ci ...`; identify the pipeline and failed jobs before reading traces. | Report the pipeline and job IDs, first actionable trace evidence per failed job, and either a confirmed cause or the next diagnostic hypothesis. |
| Releases | Use `glab release ...`. | Report the project, tag or requested range, result, whether remote state changed, and post-mutation verification when applicable. |
| Raw API | Use `glab api ...`. Classify the call by semantic effect: REST `POST`, `PUT`, `PATCH`, and `DELETE`, plus GraphQL `mutation`, are mutations; a GraphQL `query` is read-only even when transported over POST. | Report the endpoint or GraphQL operation, semantic read/write classification, response summary, and verified mutation result when applicable. |
| Archive issues | Run `<skill-dir>/scripts/archive_issues.py`; pass an explicit repository for ambiguous or self-managed hosts. | Report the project, output directory, fetched total, opened and closed counts, written count, and any collision that prevented writing. Every fetched issue must be accounted for. |

### 3. Inspect, Act, And Verify

Prefer structured output for inspection. Use these command-specific rules instead of transferring flags between commands:

| Command | Rule |
| --- | --- |
| `glab issue list` | Use `-O json` for JSON. `--all` includes opened and closed states; pagination still depends on `--page` and `--per-page`. |
| `glab mr list` | Use `-F json` for JSON. Open merge requests are the default; use `--closed` or `--merged` for other states. |
| Nested namespace | Pass explicit `-R group/subgroup/repo` or a full project URL when repository resolution is not already certain. |

Perform remote mutations only when the request authorizes the action and Step 1 resolved the target. After a mutation, query GitLab again when the resulting state is observable.

Use branch completion fields as internal checks; report the requested result, useful identifiers or links, and material uncertainty without listing irrelevant fields.

Completion criterion: every requested operation is accounted for, and every mutation is either verified or explicitly reported as unverifiable with the reason.
