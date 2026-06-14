<#
  setup-schedule.ps1  -  one-time: register the Git Bridge auto-sync scheduled task.

  RUN ONCE AS ADMINISTRATOR:
    - Press Start, type "PowerShell", right-click "Windows PowerShell" -> "Run as administrator"
    - then run:
        powershell -ExecutionPolicy Bypass -File "C:\Users\Chad\Dropbox\razorblade_mermaid\WORKFLOWS\git-bridge\setup-schedule.ps1"

  Creates task 'razorblade-os-sync' that runs seed-repo.ps1 at logon + daily at 12:00,
  as you, un-elevated (RunLevel Limited) so it can use your stored git credential,
  only when you are logged on. Creating the task needs admin; the task itself does not.

  To change the schedule later: Task Scheduler (taskschd.msc) -> Task Scheduler Library
  -> razorblade-os-sync -> Triggers. To remove: Unregister-ScheduledTask -TaskName 'razorblade-os-sync'.
#>
$ErrorActionPreference = 'Stop'

$script  = 'C:\Users\Chad\Dropbox\razorblade_mermaid\WORKFLOWS\git-bridge\seed-repo.ps1'
$logfile = 'C:\Users\Chad\Dropbox\razorblade_mermaid\WORKFLOWS\git-bridge\sync.log'
if (-not (Test-Path $script)) { throw "seed-repo.ps1 not found at $script" }

$arg       = '-ExecutionPolicy Bypass -NonInteractive -WindowStyle Hidden -File "' + $script + '"'
$action    = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $arg
$triggers  = @((New-ScheduledTaskTrigger -AtLogOn), (New-ScheduledTaskTrigger -Daily -At '12:00'))
$principal = New-ScheduledTaskPrincipal -UserId ("$env:USERDOMAIN\$env:USERNAME") -LogonType Interactive -RunLevel Limited
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

$reg = @{
  TaskName    = 'razorblade-os-sync'
  Action      = $action
  Trigger     = $triggers
  Principal   = $principal
  Settings    = $settings
  Description = 'Git Bridge: sync Obsidian vault to GitHub (razorblade-os + razorblade-skills)'
  Force       = $true
}
Register-ScheduledTask @reg | Out-Null
Write-Host ("Created task 'razorblade-os-sync' - runs at logon + daily 12:00, as " + $env:USERNAME + " (un-elevated).") -ForegroundColor Green

Write-Host "Test-running it once now..." -ForegroundColor Cyan
Start-ScheduledTask -TaskName 'razorblade-os-sync'
Start-Sleep -Seconds 10
if (Test-Path $logfile) {
  Write-Host "--- last lines of sync.log ---" -ForegroundColor DarkGray
  Get-Content $logfile -Tail 3
} else {
  Write-Host "(no sync.log yet - open Task Scheduler and check the task's Last Run Result)" -ForegroundColor Yellow
}
