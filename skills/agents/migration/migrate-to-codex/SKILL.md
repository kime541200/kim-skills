---
name: migrate-to-codex
description: Migrate supported instruction files, skills, agents, and MCP config into Codex project and global files.
disable-model-invocation: true
---

# Migrate to Codex

## Autonomy

Keep going until the selected migration is completely done: run the migrator, inspect the report, fix migrated Codex instructions/skills/agents/MCP config, and re-run checks without stopping to ask for confirmation of the next step. If the user has selected a target, do not ask before creating, editing, replacing, or deleting generated Codex artifacts in that target (`AGENTS.md`, `.codex/`, `.agents/`, or `~/.codex/`). Preserve unrelated existing Codex config entries in `.codex/config.toml` or `~/.codex/config.toml`, such as `notify`, `projects`, `marketplaces`, or unrelated MCP servers; do not ask about them unless they fail validation or directly conflict with the migration. Do not edit source Claude Code files (`.claude/`, `~/.claude/`, `.mcp.json`, or `.claude.json`), unrelated project code, secrets, or another repository.

## Migration Order

Run the migration in this order for each selected global or project source:

1. Track the selected migration with the host's available planning tool, or a short in-conversation checklist when no planning tool is available. Use concrete source → target labels. Do not create TODO files unless requested. Mark completed work and report unresolved items before finishing.

2. Read `references/differences.md` (and refresh Codex docs if its `Docs last checked` date is old).

3. Scan and inspect before writing:
   - `--scan-only` lists active and inactive source surfaces.
   - `--plan` prints staged Codex artifact paths and report rows.
   - `--doctor` summarizes readiness, manual-review work, and validation risks.

4. Convert surfaces in the same order the CLI uses:
   - instructions: `CLAUDE.md` / `AGENTS.md` to `AGENTS.md`
   - plugins: report Claude plugin trees and marketplaces as manual migration work
   - hooks: rewrite supported Claude hooks into `.codex/hooks.json` and enable `[features].codex_hooks = true`
   - skills and commands: write Codex skills under `.agents/skills/`
   - config: write `.codex/config.toml` from Claude model/sandbox settings and MCP servers, including `personality = "friendly"` when config is generated
   - subagents: write Codex custom agents under `.codex/agents/`

5. Dry-run, then write the selected target. Use `--replace` only when orphan generated skills or agents should be deleted.

6. Inspect the terminal output and `.codex/migrate-to-codex-report.txt` after real runs.

7. Review generated artifacts in this order: `AGENTS.md`, `.agents/skills/`, `.codex/config.toml`, `.codex/hooks.json`, `.codex/agents/`, then report-only plugin items.

8. Run `--validate-target` against each target after edits.

9. Re-run affected checks after edits. A later `--dry-run` compares generated output with the target; it does not authorize overwriting manual corrections.

10. Return the final migration report as one markdown table per scope that has rows. The tables cover only the non-native follow-up migration work you performed, such as skills created from slash commands, subagents, MCP servers, hooks, unsupported/local plugin notes, and manual-review caveats. Include programmatic native import rows for config, instructions, skills, or supported plugins only if you personally migrated them in this follow-up run.

    If only one scope has rows, render only the table with no heading. If multiple scopes have rows, render one heading before each table. Use `**User Config**` for user-scope rows. For project-scope rows, use the actual project folder name as the heading, for example `**northstar-support-portal**`; do not use `Current Project` as the heading. Do not add prose before or after the table output.

    Use exactly these columns:

    **northstar-support-portal**

    | Status | Item | Notes |
    | --- | --- | --- |
    | `Added` | `Slash command` pr-review | Converted into a Codex skill |
    | `Added` | `Subagent` release-lead | Added as a Codex subagent |
    | `Check before using` | `Hook` PreToolUse | Converted, but some Claude hook behavior differs in Codex |
    | `Not Added` | `Hook` Notification | Codex does not have an equivalent notification hook |
    | `Not Added` | `Plugin` team-macros | Plugin needs manual setup |

    `Status` must be `Added`, `Check before using`, or `Not Added`. Use `Added` when a Codex-facing artifact was created or changed and needs no special review. Use `Check before using` when a Codex-facing artifact was created or changed but the migration changed semantics, inferred behavior, preserved tool rules as guidance, or dropped unsupported behavior. Use `Not Added` when a source artifact was detected but no Codex-facing artifact was created. `Item` combines the artifact type and concrete item name in one cell. Artifact type must be singular: `Skill`, `Slash command`, `Subagent`, `MCP`, `Hook`, or `Plugin`. Wrap the artifact type in inline code; write the item name as plain text after it. `Notes` is always required; never leave it empty. Keep notes short, plain, and literal. Avoid internal implementation terms such as runtime expansion. Prefer phrases like `Converted into a Codex skill`, `Added as a Codex subagent`, `Added to Codex config`, `Converted into a Codex hook`, `Converted, but some Claude hook behavior differs in Codex`, `Codex does not have an equivalent notification hook`, `Plugin needs manual setup`, or `Plugin marketplace needs manual setup`.

## Fix and validate

After the initial write, resolve actionable generated-artifact issues and run `--validate-target`. Preserve manual corrections: the migrator regenerates files from the source and can overwrite corrected target files. Run it for real again only when regeneration is needed and the corrections can be preserved or reapplied within the authorized scope.

Repeat affected validation after a correction. If the same failure recurs without new evidence or a viable fix, report the blocker and continue independent authorized work. Leave source-provider changes and unresolved product choices as specific manual-review items. Do not edit source Claude files or unrelated artifacts.

## Commands

Resolve `<skill-dir>` to the absolute directory containing this SKILL.md, then set the script path.

   ```bash
   MIGRATE_TO_CODEX_SCRIPT='<skill-dir>/scripts/migrate-to-codex.py'
   ```

Inspect the migration before writing.

   ```bash
   python3 "$MIGRATE_TO_CODEX_SCRIPT" --source ~/.claude/ --scan-only
   python3 "$MIGRATE_TO_CODEX_SCRIPT" --source ~/.claude/ --target ~/.codex/ --plan
   python3 "$MIGRATE_TO_CODEX_SCRIPT" --source ~/.claude/ --target ~/.codex/ --doctor
   ```

Dry-run, then run without `--dry-run`, for global and project.

   ```bash
   python3 "$MIGRATE_TO_CODEX_SCRIPT" --source ~/.claude/ --target ~/.codex/ --dry-run
   python3 "$MIGRATE_TO_CODEX_SCRIPT" --source ~/.claude/ --target ~/.codex/
   python3 "$MIGRATE_TO_CODEX_SCRIPT" --source ./.claude/ --target ./.codex/ --dry-run
   python3 "$MIGRATE_TO_CODEX_SCRIPT" --source ./.claude/ --target ./.codex/
   ```

Run the post-migration validator against each target after edits.

   ```bash
   python3 "$MIGRATE_TO_CODEX_SCRIPT" --validate-target ~/.codex/
   python3 "$MIGRATE_TO_CODEX_SCRIPT" --validate-target ./.codex/
   ```

Run `python3 "$MIGRATE_TO_CODEX_SCRIPT" --help` for flags (`--scan-only`, `--plan`, `--doctor`, `--validate-target`, defaults, and so on). Deep tables and more links are in `references/differences.md`.
