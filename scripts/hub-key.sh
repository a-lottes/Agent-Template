#!/bin/bash
# apiKeyHelper for the adesso AI Hub. Prints the key from, in this order:
#   1. $ADESSO_AI_HUB_KEY
#   2. the macOS Keychain (service "adesso-ai-hub", see: scripts/provider.sh set-key)
#   3. an existing hub setup in ~/.claude/settings.json (env.ANTHROPIC_AUTH_TOKEN, only if its
#      ANTHROPIC_BASE_URL points to the same hub as providers/.hub-url)
if [ -n "${ADESSO_AI_HUB_KEY:-}" ]; then
  echo "$ADESSO_AI_HUB_KEY"
  exit 0
fi
if security find-generic-password -s adesso-ai-hub -w 2>/dev/null; then
  exit 0
fi
HUB_URL_FILE="$(cd "$(dirname "$0")/.." && pwd)/providers/.hub-url"
python3 - "$HUB_URL_FILE" <<'PY' && exit 0
import json, os, sys
try:
    hub = open(sys.argv[1]).read().strip().rstrip("/")
    env = json.load(open(os.path.expanduser("~/.claude/settings.json"))).get("env", {})
    if hub and env.get("ANTHROPIC_BASE_URL", "").rstrip("/") == hub and env.get("ANTHROPIC_AUTH_TOKEN"):
        print(env["ANTHROPIC_AUTH_TOKEN"]); sys.exit(0)
except Exception:
    pass
sys.exit(1)
PY
echo "No AI Hub key found. Run: scripts/provider.sh set-key" >&2
exit 1
