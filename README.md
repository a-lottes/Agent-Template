# project-memory (Claude plugin)

Turns meeting notes and documents into decisions, actions and risks. Demo plugin for "Claude Plugins, Skills & Agents Hands-on".

## Live demo (BL-AT 2026)

Step-by-step guide for building and extending this plugin live, including the adesso AI Hub: [docs/demo/ANLEITUNG.md](docs/demo/ANLEITUNG.md) (German). Prompts as files: [docs/demo/prompts/](docs/demo/prompts/README.md).

## What is inside

| Component | File | Model |
|---|---|---|
| Skill | `skills/meeting-to-actions` | main session |
| Subagent: triage | `agents/doc-triage.md` | haiku (cheap, fast) |
| Subagent: extractor | `agents/action-extractor.md` | sonnet (balanced) |
| Subagent: reviewer | `agents/reviewer.md` | opus (strict, accurate) |
| Commands | `/project-memory:process-inbox`, `/project-memory:weekly-status` | main session |
| Hooks | path guard, PII scan, audit log | none (scripts) |

Model per subagent is set in the frontmatter (`model:`). Allowed values: `haiku`, `sonnet`, `opus`, `inherit` or a full model ID. For the sovereign setup in Part 2, the model aliases can be mapped to AI Hub models.

## Try it

Separate workspace layout for unattended runs (the automation scripts below assume `~/agent-demo`):

```
~/agent-demo/
├── .claude/settings.json   # AI Hub connection (automation/ai-hub)
├── CLAUDE.md               # from examples/
├── inbox/                  # new notes land here
├── memory/                 # agent output, audit.log, runs.log
└── project-memory/         # this plugin
```

```bash
mkdir -p ~/agent-demo/{inbox,memory,.claude} && cd ~/agent-demo
cp -r /path/to/project-memory .
cp project-memory/examples/CLAUDE.md .
cp project-memory/automation/ai-hub/settings.example.json .claude/settings.json   # fill in placeholders
claude --plugin-dir ./project-memory
```

Then run `/project-memory:process-inbox` and afterwards `/project-memory:weekly-status`.

Expected: decisions, actions and risks appear in `memory/`; the reviewer rejects anything the notes do not support; the audit log fills `memory/audit.log`. Try asking Claude to write to `/tmp/x.md` to see the path guard block it, or put an e-mail address in a note to see the PII scan.

## Automation

| Folder | What |
|---|---|
| `automation/ai-hub` | Settings to run Claude Code against the adesso AI Hub (LiteLLM) |
| `automation/macos` | `run.sh` + launchd job: daily 07:00 and on every new inbox file |
| `automation/windows` | `run.ps1` + Task Scheduler: daily 07:00, inbox watcher at logon |
| `automation/sdk` | Same run from Python via the Claude Agent SDK |

Headless run used by all triggers:

```bash
claude -p "/project-memory:process-inbox" --plugin-dir ./project-memory --permission-mode acceptEdits
```

## Package for a team

This repo is also a marketplace (`.claude-plugin/marketplace.json`):

```
/plugin marketplace add <repo path or git URL>
/plugin install project-memory@adesso-agent-demo
```
