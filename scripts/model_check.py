#!/usr/bin/env python3
"""Check which AI Hub models are usable for Claude Code: reachable, fast, able to call tools.

    scripts/model_check.py                 # all chat models the key can see
    scripts/model_check.py qwen-3.6-35b-sovereign claude-opus-5

Uses the endpoint of the adesso-hub profile (see provider.sh set-url) and the key from scripts/hub-key.sh.
"""
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from provider import load_profile  # noqa: E402

BASE = load_profile("adesso-hub")["env"]["ANTHROPIC_BASE_URL"].rstrip("/")
KEY = subprocess.run([str(REPO / "scripts" / "hub-key.sh")], capture_output=True, text=True).stdout.strip()
if not KEY:
    sys.exit("No AI Hub key. Run: scripts/provider.sh set-key")

TOOL = {
    "name": "add_action",
    "description": "Record an action item from a meeting.",
    "input_schema": {
        "type": "object",
        "properties": {"action": {"type": "string"}, "owner": {"type": "string"}, "due": {"type": "string"}},
        "required": ["action", "owner", "due"],
    },
}
NOTE = "Meeting note: 'Ben will deliver the interface specification by 19 Oct 2026.' Record the action with the tool. Use ISO dates."


def call(path: str, body: dict = None) -> tuple:
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"Bearer {KEY}", "x-api-key": KEY,
                 "anthropic-version": "2023-06-01", "content-type": "application/json"},
    )
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.load(resp), time.time() - start
    except urllib.error.HTTPError as err:
        detail = json.loads(err.read() or b"{}").get("error", {})
        return {"error": detail.get("type") or err.code}, time.time() - start
    except Exception as err:  # network, timeout
        return {"error": type(err).__name__}, time.time() - start


def check(model: str) -> dict:
    data, secs = call("/v1/messages", {"model": model, "max_tokens": 1024, "tools": [TOOL],
                                       "messages": [{"role": "user", "content": NOTE}]})
    if "error" in data:
        return {"model": model, "ok": "✗", "secs": secs, "tools": "-", "detail": str(data["error"])}
    uses = [c for c in data.get("content", []) if c.get("type") == "tool_use"]
    args = uses[0]["input"] if uses else {}
    correct = args.get("owner") == "Ben" and args.get("due") == "2026-10-19"
    return {"model": model, "ok": "✓", "secs": secs,
            "tools": "✓" if correct else ("~" if uses else "✗"),
            "detail": json.dumps(args, ensure_ascii=False) if uses else "no tool call"}


def main() -> None:
    models = sys.argv[1:]
    if not models:
        listing, _ = call("/v1/models")
        models = [m["id"] for m in listing.get("data", []) if "embedding" not in m["id"]]
    print(f"Endpoint: {BASE}\n")
    print(f"{'model':<34} {'reach':<6} {'secs':>5}  {'tools':<6} detail")
    print("-" * 100)
    for model in models:
        r = check(model)
        print(f"{r['model']:<34} {r['ok']:<6} {r['secs']:>5.1f}  {r['tools']:<6} {r['detail'][:60]}")
    print("\ntools: ✓ correct call (owner Ben, due 2026-10-19) · ~ called, wrong args · ✗ no call")


if __name__ == "__main__":
    main()
