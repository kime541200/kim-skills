#!/usr/bin/env bash
set -euo pipefail

# Clone every missing child repo into the Home Repo root (the parent of scripts/).
OWNER="${GITHUB_OWNER:-<OWNER>}"
REPOS=(
  <repo-1>
  <repo-2>
)

cd "$(dirname "${BASH_SOURCE[0]}")/.."

for repo in "${REPOS[@]}"; do
  if [[ -d "$repo/.git" ]]; then
    echo "[skip] $repo"
  elif command -v gh >/dev/null 2>&1; then
    gh repo clone "$OWNER/$repo" "$repo"
  else
    git clone "https://github.com/$OWNER/$repo.git" "$repo"
  fi
done
