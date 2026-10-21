#!/bin/bash
# Creates or resets the live demo workspace (default ~/agent-demo).
# Run it after every branch switch: it copies the plugin of the current branch.
#
#   demo/setup-workspace.sh                 # create / reset (fresh inbox, empty memory)
#   demo/setup-workspace.sh --plugin-only   # only refresh the plugin, keep memory/
#   DEMO_WS=~/other demo/setup-workspace.sh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
WS="${DEMO_WS:-$HOME/agent-demo}"

mkdir -p "$WS"/{inbox,later,memory,.claude}

# The plugin is copied (not linked) into the workspace: Claude Code treats files behind a
# symlink as outside the project and would ask before every script run.
[ -L "$WS/project-memory" ] && rm "$WS/project-memory"
rsync -a --delete --exclude .git --exclude 'evals/results' "$REPO/" "$WS/project-memory/"
if [ "${1:-}" = "--plugin-only" ]; then
  echo "Plugin refreshed from branch $(git -C "$REPO" branch --show-current): $WS/project-memory"
  exit 0
fi

# Fresh input and empty memory (only inside the workspace).
find "${WS:?}/memory" -mindepth 1 -delete
find "${WS:?}/inbox" "${WS:?}/later" -mindepth 1 -delete
cp "$REPO"/examples/inbox/*.md "$WS/inbox/"
cp "$REPO"/examples/later/*.md "$WS/later/"
cp "$REPO/examples/CLAUDE.md" "$WS/CLAUDE.md"

# Project settings shared by all providers. The provider itself lives in
# .claude/settings.local.json (see scripts/provider.sh from branch demo/01-ai-hub on).
# allow: the skill's own scripts run without a prompt (PDF export, GitHub issues).
SCRIPTS="$WS/project-memory/skills/meeting-to-actions/scripts"
cat > "$WS/.claude/settings.json" <<EOF
{
  "permissions": {
    "allow": [
      "Bash(python3 $SCRIPTS/md_to_pdf.py *)",
      "Bash(python3 $SCRIPTS/create_issues.py *)",
      "Bash(python3 project-memory/skills/meeting-to-actions/scripts/md_to_pdf.py *)",
      "Bash(python3 project-memory/skills/meeting-to-actions/scripts/create_issues.py *)",
      "Bash(python3 ./project-memory/skills/meeting-to-actions/scripts/md_to_pdf.py *)",
      "Bash(python3 ./project-memory/skills/meeting-to-actions/scripts/create_issues.py *)"
    ],
    "deny": ["WebFetch", "WebSearch"]
  }
}
EOF

echo "Workspace ready: $WS"
echo "  branch:   $(git -C "$REPO" branch --show-current)"
echo "  inbox:    $(ls "$WS/inbox" | tr '\n' ' ')"
echo "  later:    $(ls "$WS/later" | tr '\n' ' ')"
if [ -f "$WS/.claude/settings.local.json" ]; then
  echo "  provider: $(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('env',{}).get('DEMO_PROVIDER','custom'))" "$WS/.claude/settings.local.json" 2>/dev/null || echo custom)"
else
  echo "  provider: (none set, uses your global Claude Code settings)"
fi
echo
echo "Start: cd $WS && claude --plugin-dir ./project-memory"
