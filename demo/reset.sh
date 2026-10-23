#!/bin/bash
# Resets the repo to the start state of the live demo (run before a rehearsal or the talk).
#   demo/reset.sh
# - inbox/ with the example steering note, empty memory/ (both gitignored)
# - provider: anthropic
# - no plugin registration (it is added by the build prompt of step 02)
set -euo pipefail
cd "$(dirname "$0")/.."
CLAUDE_BIN="$(command -v claude || echo "$HOME/.local/bin/claude")"

rm -rf inbox memory
mkdir -p inbox memory
cp examples/inbox/*.md inbox/

rm -f .claude/settings.local.json.next
scripts/provider.sh use anthropic . >/dev/null
"$CLAUDE_BIN" plugin marketplace remove adesso-agent-demo >/dev/null 2>&1 || true
python3 - <<'PY'
import json
p = ".claude/settings.local.json"; d = json.load(open(p))
d.pop("enabledPlugins", None); d.pop("extraKnownMarketplaces", None)
open(p, "w").write(json.dumps(d, indent=2) + "\n")
PY

echo "Reset done on branch $(git branch --show-current)."
echo "  inbox:    $(ls inbox | tr '\n' ' ')"
echo "  provider: anthropic, plugin not registered"
echo "Open a new Claude session in this folder."
