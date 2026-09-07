# Repository instructions

- Treat this repository as the source of truth for the personal skills under `skills/`.
- Organize skills as `skills/<category>/<subcategory>/<skill-name>/`; keep at most two category levels for standard `npx skills` discovery.
- Keep each skill self-contained, including its `agents/`, `scripts/`, `references/`, and assets.
- Keep frontmatter `name` values unique. Preserve each skill's invocation policy across supported hosts.
- When adding, moving, renaming, or deleting a skill, update the README catalog and installation notes in the same change.
- After catalog changes, run `npx --yes . list` and `npx --yes . sync` to validate discovery and synchronize managed installations.
- Exclude nested repositories, `.DS_Store`, caches, secrets, generated output, and machine-specific state.
- Validate that every listed skill has a readable `SKILL.md` with YAML frontmatter before committing.
