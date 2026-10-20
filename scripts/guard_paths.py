#!/usr/bin/env python3
"""PreToolUse: only allow writes inside memory/, and never to secret files. Exit 2 = block."""
import json, os, sys

data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path", "")
root = os.path.realpath(data.get("cwd") or os.getcwd())
target = os.path.realpath(path if os.path.isabs(path) else os.path.join(root, path))
name = os.path.basename(target)

if name.startswith(".env") or name in ("credentials", "id_rsa") or name.endswith((".pem", ".key")):
    print(f"Blocked: {name} looks like a secret file.", file=sys.stderr)
    sys.exit(2)
if not target.startswith(os.path.join(root, "memory") + os.sep):
    print("Blocked: this agent may only write inside memory/.", file=sys.stderr)
    sys.exit(2)
