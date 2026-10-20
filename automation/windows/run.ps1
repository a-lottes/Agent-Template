# Headless run of the Project Memory agent. Called by Task Scheduler (see register-tasks.ps1).
$ErrorActionPreference = "Stop"

$Project = if ($env:PROJECT) { $env:PROJECT } else { Join-Path $env:USERPROFILE "agent-demo" }
$Claude  = Join-Path $env:USERPROFILE ".local\bin\claude.exe"
if (-not (Test-Path $Claude)) { $Claude = (Get-Command claude).Source }
$Lock    = Join-Path $env:TEMP "project-memory.lock"

Set-Location $Project
New-Item -ItemType Directory -Force -Path "memory" | Out-Null
$Log = Join-Path $Project "memory\runs.log"

# Do not run twice if several files arrive at once
if (Test-Path $Lock) { exit 0 }
New-Item -ItemType File -Path $Lock | Out-Null
try {
    Add-Content $Log "=== $(Get-Date -Format s) run started"
    & $Claude -p "/project-memory:process-inbox" `
        --plugin-dir (Join-Path $Project "project-memory") `
        --permission-mode acceptEdits *>> $Log
    Add-Content $Log "=== $(Get-Date -Format s) run finished"
}
finally {
    Remove-Item $Lock -ErrorAction SilentlyContinue
}
