# Watches the inbox folder and starts run.ps1 when a new file arrives.
# Started at logon by register-tasks.ps1.
$Project = if ($env:PROJECT) { $env:PROJECT } else { Join-Path $env:USERPROFILE "agent-demo" }
$Inbox   = Join-Path $Project "inbox"
$Run     = Join-Path $PSScriptRoot "run.ps1"

$watcher = New-Object System.IO.FileSystemWatcher $Inbox
$watcher.IncludeSubdirectories = $false
$watcher.EnableRaisingEvents = $true
Register-ObjectEvent -InputObject $watcher -EventName Created -SourceIdentifier InboxCreated | Out-Null

while ($true) {
    Wait-Event -SourceIdentifier InboxCreated | Out-Null
    Start-Sleep -Seconds 5    # let the copy finish and collect several files
    Get-Event -SourceIdentifier InboxCreated -ErrorAction SilentlyContinue | Remove-Event
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Run
}
