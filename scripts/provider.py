#!/usr/bin/env python3
"""Switch the demo workspace between model providers (Anthropic, adesso AI Hub).

    provider.sh                             status of the current workspace
    provider.sh <profile>                   short for: use <profile>
    provider.sh <profile> --next            stage the switch, applied on /exit (used by /provider)
    provider.sh list
    provider.sh use <profile> [workspace]   writes <workspace>/.claude/settings.local.json
    provider.sh status [workspace]
    provider.sh files <dir>                 writes one ready-to-use settings file per profile
    provider.sh set-url https://<host>      stores the AI Hub address locally (providers/.hub-url)
    provider.sh set-key                     stores the AI Hub key in the macOS Keychain
    provider.sh env <profile>               prints export lines (for evals, CI, scripts)

Profiles live in providers/*.json. The hub address is not in the repo: it comes from
$ADESSO_AI_HUB_URL or providers/.hub-url (gitignored). The workspace is $DEMO_WS, else the current folder
if it has a .claude/ folder, else ~/agent-demo.
"""
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROFILES = REPO / "providers"
DEFAULT_WS = Path(os.environ.get("DEMO_WS") or
                  (Path.cwd() if (Path.cwd() / ".claude").is_dir() else Path.home() / "agent-demo"))
PROVIDER_KEYS = ("env", "apiKeyHelper", "model")
ALIAS_KEYS = ("ANTHROPIC_MODEL", "ANTHROPIC_DEFAULT_OPUS_MODEL",
              "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_HAIKU_MODEL")


HUB_URL_FILE = PROFILES / ".hub-url"


def hub_url() -> str:
    if os.environ.get("ADESSO_AI_HUB_URL"):
        return os.environ["ADESSO_AI_HUB_URL"].rstrip("/")
    if HUB_URL_FILE.exists():
        return HUB_URL_FILE.read_text().strip().rstrip("/")
    return ""


def load_profile(name: str, strict: bool = True) -> dict:
    path = PROFILES / f"{name}.json"
    if not path.exists():
        sys.exit(f"Unknown profile '{name}'. Available: {', '.join(profile_names())}")
    text = path.read_text().replace("__REPO__", str(REPO))
    if "__HUB_URL__" in text:
        if not hub_url() and strict:
            sys.exit("No AI Hub address set. Run: scripts/provider.sh set-url https://<ai-hub-host>")
        text = text.replace("__HUB_URL__", hub_url() or "https://<ai-hub-host>")
    return json.loads(text)


def profile_names() -> list:
    return sorted(p.stem for p in PROFILES.glob("*.json"))


def describe(settings: dict) -> str:
    env = settings.get("env", {})
    url = env.get("ANTHROPIC_BASE_URL") or "api.anthropic.com (your Claude login)"
    lines = [f"  provider: {env.get('DEMO_PROVIDER', 'custom')}", f"  endpoint: {url}"]
    for alias in ("opus", "sonnet", "haiku"):
        model = env.get(f"ANTHROPIC_DEFAULT_{alias.upper()}_MODEL") or "(Anthropic default)"
        lines.append(f"  {alias:<8}→ {model}")
    return "\n".join(lines)


def warn_about_alias() -> None:
    rc = Path.home() / ".zshrc"
    if rc.exists() and "alias claude=" in rc.read_text() and "--settings" in rc.read_text():
        print("\n⚠  ~/.zshrc defines 'alias claude=… --settings …'. --settings beats this profile.\n"
              "   Comment it out (new shell) or start with: command claude")


def cmd_list(_args) -> None:
    for name in profile_names():
        print(f"{name}\n{describe(load_profile(name, strict=False))}\n")


def cmd_use(args) -> None:
    """--next: only stage the switch (.json.next); the workspace's SessionEnd hook applies it on /exit.
    Used by /provider, because Claude Code reloads settings instantly and the running turn would
    otherwise go to the new provider with the old model."""
    # The VS Code extension has no /exit (so no SessionEnd), hence switch immediately there.
    in_vscode = "vscode" in os.environ.get("CLAUDE_CODE_ENTRYPOINT", "")
    staged = "--next" in args and not in_vscode
    args = [a for a in args if a != "--next"]
    if not args:
        sys.exit("usage: provider.sh use <profile> [workspace] [--next]")
    settings = load_profile(args[0])
    ws = Path(args[1]).expanduser() if len(args) > 1 else DEFAULT_WS
    active = ws / ".claude" / "settings.local.json"
    target = active.with_name("settings.local.json.next") if staged else active
    target.parent.mkdir(parents=True, exist_ok=True)
    # Replace only the provider keys; keep everything else (e.g. the plugin registration).
    merged = {k: v for k, v in (json.loads(active.read_text()) if active.exists() else {}).items()
              if k not in PROVIDER_KEYS}
    merged.update(settings)
    target.write_text(json.dumps(merged, indent=2) + "\n")
    print(f"Wrote {target}\n{describe(settings)}")
    if staged:
        print("\nStaged. Takes effect on /exit; then `claude -c` continues this conversation on the new provider.")
    elif in_vscode:
        print("\nActive. VS Code: start a new conversation (+ in the Claude panel) to use the new provider.")
    else:
        print("\nActive from the next start. In Claude Code: /exit, then `claude -c` to continue\n"
              "this conversation on the new provider (VS Code: open a new Claude session).")
    warn_about_alias()


def cmd_status(args) -> None:
    args = [a for a in args if a != "--next"]
    ws = Path(args[0]).expanduser() if args else DEFAULT_WS
    target = ws / ".claude" / "settings.local.json"
    if not target.exists():
        print(f"No provider set in {ws} (global Claude Code settings apply).")
    else:
        print(f"Active: {target}\n{describe(json.loads(target.read_text()))}")
    staged = target.with_name("settings.local.json.next")
    if staged.exists():
        print(f"\nStaged for the next start:\n{describe(json.loads(staged.read_text()))}")
    warn_about_alias()


def cmd_set_key(_args) -> None:
    if not shutil.which("security"):
        sys.exit("No macOS Keychain. Windows: setx ADESSO_AI_HUB_KEY \"<key>\"")
    print("Paste the AI Hub key (input hidden by the Keychain prompt):")
    subprocess.run(["security", "add-generic-password", "-U", "-s", "adesso-ai-hub",
                    "-a", os.environ.get("USER", "me"), "-w"], check=True)
    print("Stored in Keychain as service 'adesso-ai-hub'.")


def cmd_set_url(args) -> None:
    if not args or not args[0].startswith("https://"):
        sys.exit("usage: provider.sh set-url https://<ai-hub-host>")
    HUB_URL_FILE.write_text(args[0].rstrip("/") + "\n")
    print(f"Stored in {HUB_URL_FILE} (gitignored).")


def cmd_env(args) -> None:
    """Print exports so tools that ignore settings files (e.g. eval sandboxes) use the profile."""
    if not args:
        sys.exit("usage: provider.sh env <profile>")
    settings = load_profile(args[0])
    for key, value in settings.get("env", {}).items():
        if value == "":
            print(f"unset {key}")
        else:
            print(f"export {key}={shlex.quote(value)}")
    if settings.get("apiKeyHelper"):
        print(f"export ANTHROPIC_AUTH_TOKEN=\"$({settings['apiKeyHelper']})\"")


def cmd_files(args) -> None:
    """One settings file per profile, for `claude --settings <file>` (no switching needed)."""
    out = Path(args[0]).expanduser() if args else DEFAULT_WS / ".claude" / "providers"
    out.mkdir(parents=True, exist_ok=True)
    for name in profile_names():
        (out / f"{name}.json").write_text(json.dumps(load_profile(name, strict=False), indent=2) + "\n")
    print(f"Wrote {len(profile_names())} settings files to {out}")


COMMANDS = {"list": cmd_list, "use": cmd_use, "status": cmd_status, "files": cmd_files,
            "set-url": cmd_set_url, "set-key": cmd_set_key, "env": cmd_env}

if __name__ == "__main__":
    args = sys.argv[1:]
    if not [a for a in args if a != "--next"]:
        cmd_status([])
    elif args[0] in COMMANDS:
        COMMANDS[args[0]](args[1:])
    elif args[0] in profile_names():
        cmd_use(args)
    else:
        sys.exit(__doc__)
