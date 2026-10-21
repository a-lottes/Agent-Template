#!/usr/bin/env python3
"""Quick skill check: run the plugin like a user would and grade the result files.

    scripts/skill_check.py anthropic no-trigger      # short live run (seconds)
    scripts/skill_check.py                           # anthropic, all cases (~2.5 min, parallel)
    scripts/skill_check.py adesso-hub                # same cases on the AI Hub

Each case runs `claude -p` in a fresh temp workspace (all cases in parallel),
then simple checks look at memory/*.md and the tool calls. Same cases as evals/,
fewer moving parts: good for a live demo. `claude plugin eval` is the full tool.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXAMPLES = REPO / "examples"
CLAUDE = shutil.which("claude") or str(Path.home() / ".local/bin/claude")
TIMEOUT = 420

EN = "Process the new meeting notes in inbox/ into the project memory."
DE = ("Im Ordner inbox/ liegt ein neues Besprechungsprotokoll. "
      "Trag bitte Entscheidungen, Aufgaben und Risiken ins Projektgedächtnis ein.")

# name: (note to put in inbox/, copy CLAUDE.md?, prompt, checks)
# check: (label, where, kind, pattern)   where: actions|tools|answer|files   kind: has|lacks
CASES = {
    "steering-notes": ("inbox/2026-10-12-steering.md", True, EN, [
        ("skill fired", "tools", "has", r"Skill\(.*meeting-to-actions"),
        ("plugin reviewer used", "tools", "has", r"project-memory:reviewer"),
        ("actions table format", "actions", "has", r"\|\s*Action\s*\|\s*Owner\s*\|\s*Due\s*\|\s*Status\s*\|\s*Source\s*\|"),
        ("ISO due date (Ben)", "actions", "has", r"Ben[^\n]*2026-10-19"),
        ("PDF saved next to Markdown", "files", "has", r"actions\.pdf"),
    ]),
    "vague-owner": ("later/2026-10-14-sprint-review.md", True, EN, [
        ("load test not given to Ben", "actions", "lacks", r"(?i)load test[^\n]*\|\s*Ben\s*\|"),
        ("ISO due date (Erik)", "actions", "has", r"Erik[^\n]*2026-10-24"),
    ]),
    "no-trigger": (None, False, "What is a RACI matrix? Answer in two sentences.", [
        ("skill not fired", "tools", "lacks", r"Skill\(.*meeting-to-actions"),
        ("question answered", "answer", "has", r"(?i)responsib|accountab"),
    ]),
}


def profile_env(profile: str) -> dict:
    out = subprocess.run([str(REPO / "scripts/provider.sh"), "env", profile],
                         capture_output=True, text=True, check=True).stdout
    env = {k: v for k, v in os.environ.items() if not k.startswith(("ANTHROPIC_", "CLAUDE_CODE_"))}
    script = out + "\nenv -0"
    dumped = subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=env, check=True).stdout
    env = dict(item.split("=", 1) for item in dumped.split("\0") if "=" in item)
    env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"  # "project memory" means memory/ here
    return env


def run_case(name: str, env: dict) -> dict:
    note, with_claude_md, prompt, checks = CASES[name]
    ws = Path(tempfile.mkdtemp(prefix=f"skill-{name}-"))
    (ws / "inbox").mkdir()
    (ws / "memory").mkdir()
    if note:
        shutil.copy(EXAMPLES / note, ws / "inbox")
    if with_claude_md:
        shutil.copy(EXAMPLES / "CLAUDE.md", ws / "CLAUDE.md")

    scripts = REPO / "skills/meeting-to-actions/scripts"
    allow = {"permissions": {"allow": [f"Bash(python3 {scripts}/md_to_pdf.py *)"]}}
    cmd = [CLAUDE, "-p", prompt, "--plugin-dir", str(REPO), "--permission-mode", "acceptEdits",
           "--setting-sources", "project,local", "--settings", json.dumps(allow), "--add-dir", str(REPO),
           "--output-format", "stream-json", "--verbose"]
    start = time.time()
    tools, answer, error = [], "", None
    try:
        proc = subprocess.run(cmd, cwd=ws, env=env, capture_output=True, text=True,
                              timeout=TIMEOUT, stdin=subprocess.DEVNULL)
        for line in proc.stdout.splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if event.get("type") == "assistant":
                for block in event["message"].get("content", []):
                    if block.get("type") == "tool_use":
                        target = block["input"].get("skill") or block["input"].get("subagent_type") or ""
                        tools.append(f"{block['name']}({target})")
            if event.get("type") == "result":
                answer = event.get("result") or ""
    except subprocess.TimeoutExpired:
        error = f"timeout after {TIMEOUT}s"

    texts = {
        "actions": (ws / "memory/actions.md").read_text() if (ws / "memory/actions.md").exists() else "",
        "files": "\n".join(p.name for p in (ws / "memory").iterdir()),
        "tools": "\n".join(tools),
        "answer": answer,
    }
    results = []
    for label, where, kind, pattern in checks:
        found = re.search(pattern, texts[where]) is not None
        results.append((label, found if kind == "has" else not found))
    return {"name": name, "secs": time.time() - start, "results": results,
            "error": error, "workspace": ws}


def main() -> None:
    args = sys.argv[1:]
    profile = args.pop(0) if args and args[0] not in CASES else "anthropic"
    names = args or list(CASES)
    env = profile_env(profile)
    print(f"Skill check · profile {profile} · model {env.get('ANTHROPIC_MODEL') or 'Anthropic default'}")
    print(f"Running {len(names)} case(s) in parallel …\n")

    with ThreadPoolExecutor(max_workers=len(names)) as pool:
        reports = list(pool.map(lambda n: run_case(n, env), names))

    total = passed = 0
    for rep in reports:
        ok = sum(1 for _, p in rep["results"] if p)
        total += len(rep["results"])
        passed += ok
        status = "✅" if ok == len(rep["results"]) else "❌"
        print(f"{status} {rep['name']:<16} {ok}/{len(rep['results'])}  ({rep['secs']:.0f}s)"
              + (f"  ⚠ {rep['error']}" if rep["error"] else ""))
        for label, p in rep["results"]:
            print(f"     {'✓' if p else '✗'} {label}")
    print(f"\nScore: {passed}/{total} checks passed. Workspaces kept in {tempfile.gettempdir()}/skill-*")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
