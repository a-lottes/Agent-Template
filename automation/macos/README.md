# macOS trigger (launchd)

```bash
# 1. Replace USERNAME in the plist, then install it
sed -i '' "s/USERNAME/$USER/g" de.adesso.project-memory.plist
cp de.adesso.project-memory.plist ~/Library/LaunchAgents/
chmod +x run.sh
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/de.adesso.project-memory.plist

# 2. Test: start once by hand, or drop a file into ~/agent-demo/inbox
launchctl kickstart gui/$(id -u)/de.adesso.project-memory
tail -f ~/agent-demo/memory/runs.log

# Remove
launchctl bootout gui/$(id -u)/de.adesso.project-memory
```

Notes: launchd does not read `~/.zshrc`, so the AI Hub settings must live in `.claude/settings.json`.
Keep the demo folder outside Desktop/Documents/Downloads, otherwise macOS privacy prompts can block background runs.
