#!/bin/bash
# SessionStart hook for Claude Code on the web.
# Displays active requirements from PROCESS.md and flags if the local clone
# is behind origin/main, so a cold session doesn't act on stale state.

set -euo pipefail

cd "$CLAUDE_PROJECT_DIR"

# Display active requirements
if [ -f "PROCESS.md" ]; then
  echo "📋 PROCESS.md — דרישות פתוחות:"
  awk '/^## דרישות פתוחות/,/^## דרישות סגורות/' PROCESS.md | head -30
  echo ""
fi

# Flag drift vs origin/main — report only, never reset automatically
# (destructive git operations require explicit user approval per CLAUDE.md).
if git rev-parse --git-dir >/dev/null 2>&1; then
  git fetch origin main --quiet 2>/dev/null || true
  behind=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo 0)
  if [ "$behind" != "0" ]; then
    echo "⚠️  הקלונה המקומית מפגרת ב-$behind commits אחרי origin/main — סנכרן לפני עבודה (git reset --hard origin/main, לאחר אישור)."
    echo ""
  fi
fi
