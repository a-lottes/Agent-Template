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

# CLAUDE.md is configuration (not memory), so it follows the branch, also with --plugin-only.
# Target repo for GitHub issues (step 04): DEMO_GH_REPO=owner/name demo/setup-workspace.sh
# Without DEMO_GH_REPO, a repo set earlier in the workspace CLAUDE.md is kept.
OLD_REPO_LINE="$(grep -s '^GitHub repo for action items:' "$WS/CLAUDE.md" | grep -v '<owner/repo>' || true)"
cp "$REPO/examples/CLAUDE.md" "$WS/CLAUDE.md"
if [ -n "${DEMO_GH_REPO:-}" ]; then
  sed -i.bak "s|<owner/repo>|$DEMO_GH_REPO|" "$WS/CLAUDE.md" && rm -f "$WS/CLAUDE.md.bak"
elif [ -n "$OLD_REPO_LINE" ]; then
  sed -i.bak "s|^GitHub repo for action items:.*|$OLD_REPO_LINE|" "$WS/CLAUDE.md" && rm -f "$WS/CLAUDE.md.bak"
fi

if [ "${1:-}" = "--plugin-only" ]; then
  echo "Plugin refreshed from branch $(git -C "$REPO" branch --show-current): $WS/project-memory"
  exit 0
fi

# Fresh input and empty memory (only inside the workspace).
find "${WS:?}/memory" -mindepth 1 -delete
find "${WS:?}/inbox" "${WS:?}/later" -mindepth 1 -delete
cp "$REPO"/examples/inbox/*.md "$WS/inbox/"
cp "$REPO"/examples/later/*.md "$WS/later/"

# Project settings shared by all providers. The provider itself lives in
# .claude/settings.local.json (see scripts/provider.sh from branch demo/01-ai-hub on).
# allow: the skill's own scripts run without a prompt (PDF export, GitHub issues).
# SessionEnd: a provider switch requested with /provider takes effect when the session ends.
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
      "Bash(python3 ./project-memory/skills/meeting-to-actions/scripts/create_issues.py *)",
      "Bash(./project-memory/scripts/provider.sh *)"
    ],
    "deny": ["WebFetch", "WebSearch"]
  },
  "hooks": {
    "SessionEnd": [
      { "hooks": [ { "type": "command", "command": "cd \"\$CLAUDE_PROJECT_DIR\" && [ -f .claude/settings.local.json.next ] && mv .claude/settings.local.json.next .claude/settings.local.json || true" } ] }
    ]
  }
}
EOF

# Provider switching inside Claude Code (/provider) and ready-made --settings files.
if [ -d "$REPO/demo/workspace/.claude/commands" ]; then
  mkdir -p "$WS/.claude/commands"
  cp "$REPO/demo/workspace/.claude/commands/"*.md "$WS/.claude/commands/"
fi
if [ -f "$REPO/scripts/provider.py" ]; then
  python3 "$REPO/scripts/provider.py" files "$WS/.claude/providers" >/dev/null
  # Default for the demo: original Anthropic models (the hub is shown, not used throughout).
  [ -f "$WS/.claude/settings.local.json" ] || python3 "$REPO/scripts/provider.py" use anthropic "$WS" >/dev/null
fi

# One-click provider switching in VS Code: Terminal > Run Task...
if [ -f "$REPO/scripts/provider.sh" ]; then
  mkdir -p "$WS/.vscode"
  cat > "$WS/.vscode/tasks.json" <<'EOF'
{
  "version": "2.0.0",
  "tasks": [
    { "label": "Provider: adesso AI Hub (souverän)", "type": "shell", "command": "${workspaceFolder}/project-memory/scripts/provider.sh use adesso-hub ${workspaceFolder}", "problemMatcher": [] },
    { "label": "Provider: adesso AI Hub (Claude)", "type": "shell", "command": "${workspaceFolder}/project-memory/scripts/provider.sh use adesso-hub-claude ${workspaceFolder}", "problemMatcher": [] },
    { "label": "Provider: Anthropic (Original)", "type": "shell", "command": "${workspaceFolder}/project-memory/scripts/provider.sh use anthropic ${workspaceFolder}", "problemMatcher": [] },
    { "label": "Provider: Status", "type": "shell", "command": "${workspaceFolder}/project-memory/scripts/provider.sh status ${workspaceFolder}", "problemMatcher": [] },
    { "label": "AI Hub: Modell-Check", "type": "shell", "command": "${workspaceFolder}/project-memory/scripts/model_check.py", "problemMatcher": [] }
  ]
}
EOF
fi

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
