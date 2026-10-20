#!/bin/bash
# Headless run of the Project Memory agent. Called by launchd (see de.adesso.project-memory.plist).
set -euo pipefail

PROJECT="${PROJECT:-$HOME/agent-demo}"
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"   # check with: which claude
LOCK="/tmp/project-memory.lock"

cd "$PROJECT"
mkdir -p memory

# Do not run twice if several files arrive at once
if ! mkdir "$LOCK" 2>/dev/null; then exit 0; fi
trap 'rmdir "$LOCK"' EXIT

echo "=== $(date '+%F %T') run started" >> memory/runs.log
"$CLAUDE_BIN" -p "/project-memory:process-inbox" \
  --plugin-dir "$PROJECT/project-memory" \
  --permission-mode acceptEdits >> memory/runs.log 2>&1
echo "=== $(date '+%F %T') run finished" >> memory/runs.log

osascript -e 'display notification "Inbox processed, see memory/" with title "Project Memory Agent"' || true
