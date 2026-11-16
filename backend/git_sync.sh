
#!/bin/bash

set -e

echo "======================================"
echo " AI CONCIERGE - GIT SYNC PIPELINE"
echo "======================================"

# 1. Find the actual Git repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)

cd "$ROOT"

echo ""
echo "Repository: $ROOT"

# 2. Identify current branch
BRANCH=$(git branch --show-current)

if [ -z "$BRANCH" ]; then
    echo "ERROR: No active Git branch."
    exit 1
fi

echo "Current branch: $BRANCH"

# 3. Check for unfinished merge or rebase
if [ -f "$(git rev-parse --git-path MERGE_HEAD)" ]; then
    echo ""
    echo "ERROR: An unfinished merge exists."
    git status
    exit 1
fi

if [ -d "$(git rev-parse --git-path rebase-merge)" ] || \
   [ -d "$(git rev-parse --git-path rebase-apply)" ]; then
    echo "ERROR: An unfinished rebase exists."
    git status
    exit 1
fi

if [ -n "$(git diff --name-only --diff-filter=U)" ]; then
    echo "ERROR: Unresolved merge conflicts."
    git status
    exit 1
fi

# 4. Protect .env
if [ -f ".env" ] && ! git check-ignore -q .env; then
    echo "ERROR: .env is not ignored."
    exit 1
fi

# 5. Display changes
echo ""
echo "Current Git status:"
git status --short

# 6. Stage changes
echo ""
echo "Staging changes..."
git add -A

# 7. Commit changes
if ! git diff --cached --quiet; then
    echo ""
    read -r -p "Enter commit message: " COMMIT_MSG

    if [ -z "$COMMIT_MSG" ]; then
        echo "ERROR: Commit message cannot be empty."
        exit 1
    fi

    git commit -m "$COMMIT_MSG"
else
    echo "No changes to commit."
fi

# 8. Check GitHub remote
echo ""
echo "Checking remote..."

if ! git remote get-url origin >/dev/null 2>&1; then
    echo "ERROR: Remote origin is not configured."
    exit 1
fi

git remote -v

# 9. Configure Windows Git Credential Manager
git config --global credential.helper manager

# 10. Fetch latest remote changes
echo ""
echo "Fetching from GitHub..."

git fetch origin

# 11. Rebase local branch
echo ""
echo "Rebasing against origin/$BRANCH..."

git rebase "origin/$BRANCH"

# 12. Push changes
echo ""
echo "Pushing to GitHub..."

git push -u origin "$BRANCH"

# 13. Final status
echo ""
echo "======================================"
echo " GIT SYNC COMPLETED SUCCESSFULLY"
echo "======================================"

git status
git log -1 --oneline
