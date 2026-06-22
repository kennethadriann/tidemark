#!/usr/bin/env bash
# TIDEMARK daily runner (Model B: write to a branch, auto-merge to main on PASS).
# Fully unattended. Intended for cron. Point this ONLY at the tidemark repo.
set -euo pipefail

REPO_DIR="${TIDEMARK_DIR:-$HOME/tidemark}"
cd "$REPO_DIR"

git checkout main
git pull --rebase origin main

# Figure out the next chapter number from existing files.
last=$(ls manuscript/ch*.md 2>/dev/null | sed -E 's/.*ch0*([0-9]+)\.md/\1/' | sort -n | tail -1)
last=${last:-0}
NN=$(printf "%02d" $(( last + 1 )))

# Weekly audit on every 7th chapter; otherwise write a chapter.
if [ $(( (10#$NN) % 7 )) -eq 0 ]; then
  claude -p "/audit" --dangerously-skip-permissions
  if [ -n "$(git status --porcelain)" ]; then
    git add -A && git commit -m "audit: after ch $NN" && git push origin main
  fi
  exit 0
fi

BRANCH="chapter/ch${NN}"
git checkout -b "$BRANCH"

claude -p "/chapter" --dangerously-skip-permissions

# Nothing produced (guard tripped / skipped day) -> clean up, exit.
if [ -z "$(git status --porcelain)" ]; then
  git checkout main
  git branch -D "$BRANCH" || true
  echo "No chapter produced (skipped). Exiting clean."
  exit 0
fi

MSG="$(cat notes/.last_commit_msg 2>/dev/null || echo "ch ${NN}: untitled")"
git add -A
git commit -m "$MSG"

if grep -q "AUDIT: PASS" notes/.last_run 2>/dev/null; then
  git checkout main
  git merge --no-ff "$BRANCH" -m "merge $MSG"
  git push origin main
  git branch -d "$BRANCH" || true
  git push origin --delete "$BRANCH" 2>/dev/null || true
  echo "PASS -> merged to main: $MSG"
else
  git push origin "$BRANCH"
  git checkout main
  echo "FAIL -> quarantined on $BRANCH for review: $MSG"
fi
