#!/bin/bash
# apiKeyHelper for the adesso AI Hub: prints the key from $ADESSO_AI_HUB_KEY or the macOS Keychain.
if [ -n "${ADESSO_AI_HUB_KEY:-}" ]; then
  echo "$ADESSO_AI_HUB_KEY"
  exit 0
fi
if security find-generic-password -s adesso-ai-hub -w 2>/dev/null; then
  exit 0
fi
echo "No AI Hub key found. Run: scripts/provider.sh set-key" >&2
exit 1
