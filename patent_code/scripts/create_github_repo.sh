#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/create_github_repo.sh [repo-name] [--private]

REPO_NAME=${1:-$(basename "$PWD")}
PRIVATE=false
if [[ ${2:-} == "--private" ]]; then
  PRIVATE=true
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install from https://cli.github.com/ and run 'gh auth login' first." >&2
  exit 1
fi

echo "Creating GitHub repo: $REPO_NAME (private=$PRIVATE)"

if $PRIVATE; then
  gh repo create "$REPO_NAME" --private --source=. --remote=origin --push -y
else
  gh repo create "$REPO_NAME" --public --source=. --remote=origin --push -y
fi

echo "Repository created and pushed. Set Actions secrets as described in PUSH_INSTRUCTIONS.md"
