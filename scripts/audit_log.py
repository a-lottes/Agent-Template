#!/usr/bin/env python3
"""PostToolUse: append every tool call to memory/audit.log (JSON lines)."""
import json, os, sys, datetime

data = json.load(sys.stdin)
root = data.get("cwd") or os.getcwd()
os.makedirs(os.path.join(root, "memory"), exist_ok=True)
entry = {
    "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "session": data.get("session_id"),
    "tool": data.get("tool_name"),
    "target": (data.get("tool_input") or {}).get("file_path") or (data.get("tool_input") or {}).get("command", "")[:120],
}
with open(os.path.join(root, "memory", "audit.log"), "a", encoding="utf-8") as f:
    f.write(json.dumps(entry) + "\n")
