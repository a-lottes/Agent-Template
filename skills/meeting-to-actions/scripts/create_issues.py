#!/usr/bin/env python3
"""Create GitHub issues for open action items in memory/actions.md, via the gh CLI.

    create_issues.py memory/actions.md --dry-run     # show what would be created
    create_issues.py memory/actions.md               # create, then write "#<n>" into Status

Target repo: --repo owner/name, else $PROJECT_MEMORY_GH_REPO, else the line
"GitHub repo for action items: owner/name" in ./CLAUDE.md, else the GitHub repo of the
current git checkout.
Rows whose Status already contains an issue reference (#123) are skipped, so re-runs are safe.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def target_repo(cli_value: str) -> str:
    if cli_value:
        return cli_value
    if os.environ.get("PROJECT_MEMORY_GH_REPO"):
        return os.environ["PROJECT_MEMORY_GH_REPO"]
    claude_md = Path("CLAUDE.md")
    if claude_md.exists():
        m = re.search(r"GitHub repo for action items:\s*`?([\w.-]+/[\w.-]+)`?", claude_md.read_text())
        if m:
            return m.group(1)
    # Last resort: the GitHub repo of the current git checkout (e.g. when running inside this repo).
    found = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
                           capture_output=True, text=True)
    if found.returncode == 0 and found.stdout.strip():
        return found.stdout.strip()
    sys.exit("No target repo. Add 'GitHub repo for action items: owner/name' to CLAUDE.md or pass --repo.")


def split_row(line: str) -> list:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("actions", type=Path)
    parser.add_argument("--repo", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = target_repo(args.repo)
    lines = args.actions.read_text(encoding="utf-8").splitlines()
    header_at = next((i for i, l in enumerate(lines) if re.match(r"^\|\s*Action\s*\|", l)), None)
    if header_at is None:
        sys.exit(f"{args.actions}: no '| Action | Owner | Due | Status | Source |' table found.")
    cols = [c.lower() for c in split_row(lines[header_at])]
    col = {name: cols.index(name) for name in ("action", "owner", "due", "status", "source") if name in cols}

    todo = []
    for i in range(header_at + 2, len(lines)):
        if not lines[i].strip().startswith("|"):
            break
        cells = split_row(lines[i])
        status = cells[col["status"]] if "status" in col else ""
        if "open" in status.lower() and not re.search(r"#\d+", status):
            todo.append((i, cells))

    if not todo:
        print("Nothing to do: every open action already has an issue.")
        return
    print(f"{'Would create' if args.dry_run else 'Creating'} {len(todo)} issue(s) in {repo}:")

    for i, cells in todo:
        get = lambda name: cells[col[name]] if name in col and col[name] < len(cells) else "TBD"
        title = get("action")
        body = (f"**Owner:** {get('owner')}  \n**Due:** {get('due')}  \n**Source:** {get('source')}\n\n"
                f"_Created by the project-memory agent from `{args.actions}`._")
        if args.dry_run:
            print(f"  - {title}  (owner {get('owner')}, due {get('due')})")
            continue
        result = subprocess.run(["gh", "issue", "create", "--repo", repo, "--title", title, "--body", body],
                                capture_output=True, text=True)
        if result.returncode != 0:
            sys.exit(f"gh failed for '{title}': {result.stderr.strip()}")
        url = result.stdout.strip().splitlines()[-1]
        number = url.rstrip("/").rsplit("/", 1)[-1]
        cells[col["status"]] = f"open · #{number}"
        lines[i] = "| " + " | ".join(cells) + " |"
        print(f"  - #{number} {title}  {url}")

    if not args.dry_run:
        args.actions.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Updated {args.actions} with issue numbers.")


if __name__ == "__main__":
    main()
