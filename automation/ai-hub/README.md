# Connect Claude Code to the adesso AI Hub (LiteLLM)

Copy `settings.example.json` to `<project>/.claude/settings.json` (only this project uses the AI Hub)
or to `~/.claude/settings.json` (all projects). Replace the placeholders.

- `ANTHROPIC_BASE_URL`: AI Hub root URL, **without** `/v1` (Claude Code appends `/v1/messages`).
- `ANTHROPIC_DEFAULT_*_MODEL`: maps the aliases `opus`, `sonnet`, `haiku` to AI Hub models.
  The subagents in this plugin (`model: haiku|sonnet|opus`) follow this mapping automatically.
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`: no telemetry, error reporting or auto-update calls.
- `permissions.deny`: no web access from the agent.

## API key

macOS (Keychain, used by `apiKeyHelper`):

```bash
security add-generic-password -s adesso-ai-hub -a "$USER" -w '<your-ai-hub-key>'
```

Windows: remove the `apiKeyHelper` line and set the key as a user environment variable instead:

```powershell
setx ANTHROPIC_AUTH_TOKEN "<your-ai-hub-key>"
```

## Check

```bash
curl -s https://<ai-hub-host>/v1/models -H "Authorization: Bearer <your-ai-hub-key>"
claude          # then /status and /model
```

## Switchable profiles (live demo)

Instead of editing settings by hand, use the profiles in `providers/` and switch per workspace:

```bash
scripts/provider.sh set-key            # once: key into the Keychain
scripts/provider.sh use adesso-hub     # or: anthropic, adesso-hub-claude
scripts/model_check.py                 # which hub models can call tools?
```

See `docs/demo/01-ai-hub/`.
