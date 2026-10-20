# Registers two scheduled tasks for the current user:
#   ProjectMemory-Daily : every day at 07:00 (catches up if the laptop was off)
#   ProjectMemory-Watch : starts the inbox watcher at logon
$Here = $PSScriptRoot
$Ps   = "powershell.exe"

$dailyAction = New-ScheduledTaskAction -Execute $Ps `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$Here\run.ps1`""
Register-ScheduledTask -TaskName "ProjectMemory-Daily" -Force `
    -Trigger (New-ScheduledTaskTrigger -Daily -At 7:00am) `
    -Action $dailyAction `
    -Settings (New-ScheduledTaskSettingsSet -StartWhenAvailable)

$watchAction = New-ScheduledTaskAction -Execute $Ps `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$Here\watch-inbox.ps1`""
Register-ScheduledTask -TaskName "ProjectMemory-Watch" -Force `
    -Trigger (New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME) `
    -Action $watchAction `
    -Settings (New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::Zero))

Write-Host "Done. Test with: Start-ScheduledTask -TaskName ProjectMemory-Daily"
