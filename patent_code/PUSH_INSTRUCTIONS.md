# Push repository to GitHub (instructions)

This file explains how to publish this local repository to GitHub and run CI.

Prerequisites

- Git installed and configured (`git config --global user.name` and `user.email`).
- GitHub CLI (`gh`) installed and authenticated (run `gh auth login`).

Quick steps (recommended, using `gh`):

1. Initialize git (if not already):

```bash
cd /path/to/patent_code
git init
git add .
git commit -m "Initial scaffold: Phase 1 & Phase 2 auth"
```

2. Create GitHub repo and push (uses `gh`):

```bash
./scripts/create_github_repo.sh my-petcare-backend
# or for private repo
./scripts/create_github_repo.sh my-petcare-backend --private
```

3. Add required GitHub Actions secrets (Settings → Secrets):

- `SECRET_KEY` — strong secret
- `DATABASE_URL` (for staging/prod)
- `TEST_DATABASE_URL` (optional for CI)
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `APPLE_CLIENT_ID`, `APPLE_CLIENT_SECRET` (if used)

4. Run CI manually: GitHub → Actions → CI → Run workflow (or push a commit).

If you cannot use `gh`, create a repo on GitHub web UI, add remote and push:

```bash
git remote add origin git@github.com:youruser/yourrepo.git
git branch -M main
git push -u origin main
```

After push

- Open Actions tab to see CI run; review logs and paste any failures here so I can fix them.
