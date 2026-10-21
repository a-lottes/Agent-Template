#!/bin/bash
# Validate and evaluate the plugin's skill against a provider profile.
#
#   scripts/eval.sh anthropic --case no-trigger   # short live run (seconds)
#   scripts/eval.sh                               # anthropic, all cases, 1 run each
#   scripts/eval.sh adesso-hub                    # same suite on the AI Hub
#   scripts/eval.sh anthropic --runs 3            # for real decisions: more runs
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PROFILE="${1:-anthropic}"
shift || true
CLAUDE_BIN="$(command -v claude || echo "$HOME/.local/bin/claude")"

# Eval runs live in a sandbox that ignores settings files, so the profile goes in as env vars.
eval "$("$REPO/scripts/provider.sh" env "$PROFILE")"
# "project memory" in our prompts means memory/, not Claude's built-in auto memory.
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1

cd "$REPO"
echo "== 1/2 validate (structure)"
"$CLAUDE_BIN" plugin validate --strict .claude-plugin/plugin.json
"$CLAUDE_BIN" plugin validate --strict skills
"$CLAUDE_BIN" plugin validate --strict agents

echo
echo "== 2/2 eval (behaviour) · profile: $PROFILE · model: ${ANTHROPIC_MODEL:-Anthropic default}"
exec "$CLAUDE_BIN" plugin eval . \
  --scaffold --trust-plugin \
  --allow-tools Write Edit \
  --ablation none --runs 1 -j 4 \
  --no-publish "$@"
