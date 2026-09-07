# Kim Skills

Personal agent skills, organized as an installable catalog for the open Agent Skills ecosystem.

## Catalog

### Agents

- **Migration**
  - `migrate-to-codex` — migrate supported Claude Code configuration and artifacts to Codex.
- **Orchestration**
  - `agy-delegate` — delegate large mechanical corpus sweeps to Antigravity CLI.
- **Prompting**
  - `optimize-prompts` — audit and improve reusable prompt artifacts.

### Engineering

- **Python**
  - `python-src-layout` — design or migrate installable Python packages to src-layout.
- **Version control**
  - `gh-cli` — operate GitHub through `gh`.
  - `gitlab-cli` — operate GitLab through `glab`.
  - `git-commit` — prepare and create scoped Git commits.
  - `git-report` — generate progress reports from Git history.

### Operations

- **System**
  - `ubuntu-cleanup` — inventory and clean reclaimable Ubuntu storage.

### Productivity

- **Accessibility**
  - `adhd-mode` — reduce reading effort and cognitive load.

## Install and synchronize

The repository includes a dependency-free `kim-skills` command. It installs copies into
`~/.agents/skills` and records only the skills managed by this repository in
`~/.agents/skills/.kim-skills.json`.

List the catalog:

```bash
npx --yes /home/kim/workspace/myproject/skills/kim-skills list
```

Install the complete catalog. This selects "all" mode, so later syncs also install newly added skills:

```bash
npx --yes /home/kim/workspace/myproject/skills/kim-skills install --all
```

Or install a selected set:

```bash
npx --yes /home/kim/workspace/myproject/skills/kim-skills install gh-cli git-commit
```

After editing the repository, synchronize installed copies:

```bash
npx --yes /home/kim/workspace/myproject/skills/kim-skills sync
```

In "all" mode, `sync` installs additions, updates changes, and removes installed copies whose source directory was deleted. In selected mode, install another skill explicitly or remove one from the managed selection:

```bash
npx --yes /home/kim/workspace/myproject/skills/kim-skills install ubuntu-cleanup
npx --yes /home/kim/workspace/myproject/skills/kim-skills remove ubuntu-cleanup
```

After publishing the repository to GitHub, the same package can run without a local checkout. Replace `OWNER` with the GitHub account or organization:

```bash
npx --yes github:OWNER/kim-skills sync
```

The standard Agent Skills CLI can also discover this repository's categorized layout:

```bash
npx skills@latest add /home/kim/workspace/myproject/skills/kim-skills --list
```

Its global Codex target is `~/.codex/skills`, and local-path installations are not source-tracked for reliable update and deletion. The repository command above therefore owns synchronization to `~/.agents/skills`.

## Maintain

- The repository is the editable source of truth. Treat `~/.agents/skills` as installed output.
- Put each skill under `skills/<category>/<subcategory>/<skill-name>/`.
- Keep category depth to two levels so the standard CLI discovers skills without `--full-depth`.
- Keep each skill's `name` unique across the repository.
- Preserve all files belonging to a skill beside its `SKILL.md`; do not commit nested `.git`, `.DS_Store`, caches, credentials, or generated output.
- Update the catalog above when adding, moving, renaming, or removing a skill.
