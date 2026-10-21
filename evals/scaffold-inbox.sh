#!/bin/bash
# Shared eval scaffold: puts one example note into inbox/ of the sandbox workspace.
#   usage (from a case's scaffold.sh): scaffold-inbox.sh <inbox|later>/<file> [--with-claude-md]
set -euo pipefail
EXAMPLES="$(cd "$(dirname "$0")/../examples" && pwd)"
mkdir -p inbox memory
cp "$EXAMPLES/$1" inbox/
if [ "${2:-}" = "--with-claude-md" ]; then
  cp "$EXAMPLES/CLAUDE.md" CLAUDE.md
fi
