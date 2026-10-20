#!/usr/bin/env python3
"""PostToolUse: scan the written file for personal data. Exit 2 feeds the message back to Claude."""
import json, re, sys

data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path", "")
try:
    text = open(path, encoding="utf-8", errors="ignore").read()
except OSError:
    sys.exit(0)

patterns = {
    "email address": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "IBAN": r"\b[A-Z]{2}\d{2}(?: ?\d{4}){3,7}(?: ?\d{1,4})?\b",
    "phone number": r"(?<!\d)(?:\+|00)\d[\d /-]{8,14}\d",
}
hits = [label for label, rx in patterns.items() if re.search(rx, text)]
if hits:
    print(f"PII check: {path} contains {', '.join(hits)}. Remove or mask it and rewrite the file.", file=sys.stderr)
    sys.exit(2)
