<#
  pack-skills.ps1  -  Git Bridge delivery leg, part 1 of 2 (SOURCE -> PACKAGE).

  Desktop PowerShell, no Python. Builds .skill packages from their editable text
  source (WORKFLOWS/skills-src/<name>/) into WORKFLOWS/skills/. Part 2 (PUSH) is
  the existing seed-repo.ps1 / razorblade-os-sync scheduled task, unchanged.

  Why desktop, not sandbox: writing a .skill into Dropbox is SAFE from the desktop
  (an ordinary local write Dropbox then syncs - it is how skills got there in the
  first place). The "no binaries into the Dropbox mount" rule (obs-058/062) is a
  SANDBOX-only hazard. The sandbox never builds or pushes - it only pulls + audits.

  First run BOOTSTRAPS skills-src/ from the current packages (one-time source
  adoption). Then the loop is:
    edit WORKFLOWS/skills-src/<name>/SKILL.md  ->  run this  ->  run seed-repo.ps1
    (or just wait for the scheduled sync)      ->  the rebuilt skill ships to GitHub.

  Change-detected: a skill is only repackaged when its source actually changed, so
  unchanged skills never churn the git history.

  Run on the DESKTOP:
    powershell -ExecutionPolicy Bypass -File "C:\Users\Chad\Dropbox\razorblade_mermaid\WORKFLOWS\git-bridge\pack-skills.ps1"
#>
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem | Out-Null

$Vault     = 'C:\Users\Chad\Dropbox\razorblade_mermaid'
$SkillsDir = Join-Path $Vault 'WORKFLOWS\skills'
$SrcDir    = Join-Path $Vault 'WORKFLOWS\skills-src'
$HashFile  = Join-Path $SrcDir '.src-hashes.json'
$Log       = Join-Path $Vault 'WORKFLOWS\git-bridge\sync.log'
$Tmp       = Join-Path $env:TEMP ('packskills_' + [guid]::NewGuid().ToString('N'))

if (-not (Test-Path $SkillsDir)) { throw "skills dir not found: $SkillsDir" }
New-Item -ItemType Directory -Force -Path $SrcDir, $Tmp | Out-Null

# content_sha256 == build.py's recipe: sha256 over sorted( utf8(relpath) + 0x00 + sha256(filebytes) ).
# Used here only as a change-detector; build.py audit recomputes from the package, so this is informational.
function Get-ContentSha($dir) {
  $sha  = [System.Security.Cryptography.SHA256]::Create()
  $base = (Resolve-Path $dir).Path
  $rels = Get-ChildItem $dir -Recurse -File |
          ForEach-Object { $_.FullName.Substring($base.Length + 1).Replace('\','/') } | Sort-Object
  $ms = New-Object System.IO.MemoryStream
  foreach ($rel in $rels) {
    $rb = [Text.Encoding]::UTF8.GetBytes($rel)
    $ms.Write($rb, 0, $rb.Length); $ms.WriteByte(0)
    $fh = $sha.ComputeHash([IO.File]::ReadAllBytes((Join-Path $base $rel)))
    $ms.Write($fh, 0, $fh.Length)
  }
  -join ($sha.ComputeHash($ms.ToArray()) | ForEach-Object { $_.ToString('x2') })
}

# --- 1. Bootstrap skills-src/ from any package that has no source yet ---
foreach ($p in (Get-ChildItem $SkillsDir -Filter *.skill)) {
  $name = $p.BaseName
  $dst  = Join-Path $SrcDir $name
  if (Test-Path $dst) { continue }
  $ex = Join-Path $Tmp ("ex_" + $name)
  [System.IO.Compression.ZipFile]::ExtractToDirectory($p.FullName, $ex)
  $inner = Join-Path $ex $name          # package root is <name>/...
  if (Test-Path $inner) { Move-Item $inner $dst }
  else { New-Item -ItemType Directory -Force -Path $dst | Out-Null; Move-Item (Join-Path $ex '*') $dst -Force }
  Write-Host "  bootstrapped source: skills-src\$name" -ForegroundColor DarkCyan
}

# --- 2. Load change-detector state ---
$hashes = @{}
if (Test-Path $HashFile) {
  (Get-Content $HashFile -Raw | ConvertFrom-Json).PSObject.Properties | ForEach-Object { $hashes[$_.Name] = $_.Value }
}

# --- 3. Rebuild any skill whose source changed (or whose .skill is missing) ---
$rebuilt = @()
foreach ($d in (Get-ChildItem $SrcDir -Directory)) {
  $name   = $d.Name
  $h      = Get-ContentSha $d.FullName
  $pkg    = Join-Path $SkillsDir "$name.skill"
  $stored = $hashes[$name]
  if (Test-Path $pkg) {
    if ($null -eq $stored) { $hashes[$name] = $h; continue }   # first run: adopt existing package as current (no churn)
    if ($stored -eq $h)    { continue }                        # source unchanged
  }
  # source changed, or package missing -> rebuild
  $zip = Join-Path $Tmp "$name.skill"
  if (Test-Path $zip) { Remove-Item $zip -Force }
  # includeBaseDirectory = $true  ->  entries are "<name>/<rel>" with forward slashes (cross-platform safe)
  [System.IO.Compression.ZipFile]::CreateFromDirectory($d.FullName, $zip,
     [System.IO.Compression.CompressionLevel]::Optimal, $true)
  Copy-Item $zip $pkg -Force
  $hashes[$name] = $h
  $rebuilt += $name
  Write-Host "  packaged: $name.skill" -ForegroundColor Green
}

# --- 4. Persist state + clean up ---
($hashes | ConvertTo-Json) | Set-Content $HashFile -Encoding ASCII
Remove-Item $Tmp -Recurse -Force -ErrorAction SilentlyContinue

if ($rebuilt.Count) {
  Write-Host ("Rebuilt {0} skill(s): {1}." -f $rebuilt.Count, ($rebuilt -join ', ')) -ForegroundColor Cyan
  Write-Host "Now run seed-repo.ps1 (or wait for the scheduled sync) to push them to GitHub." -ForegroundColor Cyan
  ("{0}  PACK  rebuilt={1}" -f (Get-Date -Format 'o'), ($rebuilt -join ',')) | Add-Content $Log
} else {
  Write-Host "No skill source changed - nothing to repackage." -ForegroundColor Yellow
}
