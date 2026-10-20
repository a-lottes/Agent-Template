# Windows trigger (Task Scheduler)

```powershell
# 1. Register both tasks (run in a normal PowerShell, no admin needed)
cd $env:USERPROFILE\agent-demo\project-memory\automation\windows
powershell -ExecutionPolicy Bypass -File .\register-tasks.ps1

# 2. Test
Start-ScheduledTask -TaskName ProjectMemory-Daily
Get-Content $env:USERPROFILE\agent-demo\memory\runs.log -Wait

# Start the watcher now (otherwise it starts at next logon)
Start-ScheduledTask -TaskName ProjectMemory-Watch

# Remove
Unregister-ScheduledTask -TaskName ProjectMemory-Daily -Confirm:$false
Unregister-ScheduledTask -TaskName ProjectMemory-Watch -Confirm:$false
```

Notes: the hooks call `python3`. If Windows only knows `python` or `py`, change the commands in `hooks/hooks.json`.
Set the AI Hub key with `setx ANTHROPIC_AUTH_TOKEN "<key>"` (see `../ai-hub/README.md`); scheduled tasks of your user see it after the next logon.
