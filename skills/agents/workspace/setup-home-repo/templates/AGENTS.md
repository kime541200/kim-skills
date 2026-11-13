# <workspace>: <one-line purpose> (Home Repo)

This directory is the **Home Repo** (`<OWNER>/<workspace>`), the agent launch base. Each child directory is an independent GitHub repo, ignored in the root `.gitignore`, never a submodule.

| Directory | Role | Repo |
| --- | --- | --- |
| `<repo-1>/` | <role> | https://github.com/<OWNER>/<repo-1> |

## Navigation

- **On-demand clone**: when a needed child directory is missing, run `gh repo clone <OWNER>/<repo>`, or `./scripts/clone-all.sh` for all.
- **Precedence**: read a child's `AGENTS.md` before working in it; the child's rules win over this file.
- **Routes**: <task type> → follow `<repo>/AGENTS.md`.
- **Docs**: `docs/` for usage, `GLOSSARY.md` for shared terms, `docs/adr/` for decisions.

## Cross-repo flow

1. <how the children hand work to each other>

## Rules for the children

- Reference other children by full GitHub URL in docs; no `../<repo>` paths or absolute local paths in code, compose files or docs.
- Wire cross-service connections through environment variables (ship `.env.example`) or CLI parameters.
- Create repos `--private` first; list the files to the user before `gh repo create` or `git push`.
