#!/usr/bin/env python3
"""PreToolUse: only allow writes inside memory/ and inbox/, and never to secret files. Exit 2 = block.

Developer mode: when Claude runs inside the plugin's own source folder (you are building the
plugin), writes to the plugin files are allowed too. Secret files stay blocked everywhere.
"""
import json, os, sys

data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path", "")
root = os.path.realpath(data.get("cwd") or os.getcwd())
target = os.path.realpath(path if os.path.isabs(path) else os.path.join(root, path))
name = os.path.basename(target)
plugin_root = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

if name.startswith(".env") or name in ("credentials", "id_rsa") or name.endswith((".pem", ".key")):
    print(f"Blocked: {name} looks like a secret file.", file=sys.stderr)
    sys.exit(2)
if root == plugin_root and target.startswith(root + os.sep):
    sys.exit(0)  # developer mode: building the plugin itself
if not any(target.startswith(os.path.join(root, d) + os.sep) for d in ("memory", "inbox")):
    print("Blocked: this agent may only write inside memory/ and inbox/.", file=sys.stderr)
    sys.exit(2)
