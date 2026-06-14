<#
  seed-repo.ps1  -  Git Bridge seed + ongoing sync (razorblade-os + razorblade-skills)

  Run on your DESKTOP from PowerShell. One-way mirror: Obsidian vault -> repos -> GitHub.
    - razorblade-os      (PRIVATE) : full OS mirror (brain docs + WORKFLOWS + skills + manifest) = your restore floor
    - razorblade-skills  (PUBLIC)  : tooling only (WORKFLOWS canon + skills + manifest) = what the Cowork sandbox pulls

  Safe to re-run any time - it doubles as the sync step (only commits when something changed).

  Usage:
    powershell -ExecutionPolicy Bypass -File "C:\Users\Chad\Dropbox\razorblade_mermaid\WORKFLOWS\git-bridge\seed-repo.ps1"
#>

$ErrorActionPreference = 'Stop'

$Vault      = 'C:\Users\Chad\Dropbox\razorblade_mermaid'
$RepoOS     = 'C:\Users\Chad\razorblade-os'       # private full mirror
$RepoSkills = 'C:\Users\Chad\razorblade-skills'   # public tooling mirror

$brain = '_ME.md','_VAULT MAP.md','_SKILLS MAP.md','_DIRECTIVES.md',
         '_OBSERVATIONS.md','_BACKLOG.md','_CHANGELOG.md'
$wfSrc = Join-Path $Vault 'WORKFLOWS'

function Assert-Repo($p) {
  if (-not (Test-Path $p))                    { throw "Repo not found at $p (create it on GitHub and clone it to this path first)" }
  if (-not (Test-Path (Join-Path $p '.git'))) { throw "$p is not a git working copy" }
}

# Write UTF-8 WITHOUT a BOM (PS 5.1 Set-Content -Encoding UTF8 adds one, which breaks Python json.load downstream)
function Write-Utf8NoBom($path, $text) {
  [System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))
}

function Copy-Workflows($repo) {
  $wfDst = Join-Path $repo 'WORKFLOWS'
  New-Item -ItemType Directory -Force -Path $wfDst | Out-Null
  Copy-Item (Join-Path $wfSrc '*.md') $wfDst -Force
  $sSrc = Join-Path $wfSrc 'skills'
  if (Test-Path $sSrc) {
    $sDst = Join-Path $wfDst 'skills'
    New-Item -ItemType Directory -Force -Path $sDst | Out-Null
    Copy-Item (Join-Path $sSrc '*.skill') $sDst -Force
  }
  # Git Bridge tooling (build.py + this script) so the sandbox pulls them with the repo
  $gSrc = Join-Path $wfSrc 'git-bridge'
  if (Test-Path $gSrc) {
    $gDst = Join-Path $wfDst 'git-bridge'
    New-Item -ItemType Directory -Force -Path $gDst | Out-Null
    foreach ($t in 'build.py','seed-repo.ps1') {
      $tp = Join-Path $gSrc $t
      if (Test-Path $tp) { Copy-Item $tp $gDst -Force }
    }
  }
  return (Join-Path $wfDst 'skills')
}

function New-Manifest($skillsDir, $outFile) {
  $skills = @()
  if (Test-Path $skillsDir) {
    Get-ChildItem $skillsDir -Filter *.skill | Sort-Object Name | ForEach-Object {
      $skills += [ordered]@{
        name    = $_.BaseName
        package = "WORKFLOWS/skills/$($_.Name)"
        sha256  = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower()
        bytes   = $_.Length
      }
    }
  }
  $m = [ordered]@{
    generated = (Get-Date -Format 'o')
    note      = 'sha256 = desktop-side hash of each built .skill package; skill-audit compares installed-vs-this.'
    skills    = $skills
  }
  Write-Utf8NoBom $outFile ($m | ConvertTo-Json -Depth 6)
  return $skills.Count
}

function Write-GitAttributes($repo) {
  "* text=auto eol=lf`r`n*.skill binary`r`n" | Set-Content (Join-Path $repo '.gitattributes') -Encoding ASCII -NoNewline
}

function Commit-Push($repo, $msg) {
  Push-Location $repo
  try {
    git add --renormalize . 2>$null | Out-Null
    git add -A
    if (git status --porcelain) {
      git commit -m $msg | Out-Host
      git branch -M main
      git push -u origin main | Out-Host
      Write-Host "  pushed: $repo" -ForegroundColor Green
    } else {
      Write-Host "  no changes: $repo" -ForegroundColor Yellow
    }
  } finally {
    Pop-Location
  }
}

Assert-Repo $RepoOS
Assert-Repo $RepoSkills
$stamp = Get-Date -Format 'yyyy-MM-dd HH:mm'

# ---- razorblade-os (PRIVATE, full mirror) ----
Write-Host "== razorblade-os (private) ==" -ForegroundColor Cyan
foreach ($f in $brain) {
  $src = Join-Path $Vault $f
  if (Test-Path $src) {
    Copy-Item $src (Join-Path $RepoOS $f) -Force
    $len = (Get-Item (Join-Path $RepoOS $f)).Length
    if ($len -lt 200) { Write-Warning "  $f is only $len bytes - check for truncation" }
  } else { Write-Warning "  missing brain doc: $f" }
}
$skOS = Copy-Workflows $RepoOS
$nOS  = New-Manifest $skOS (Join-Path $RepoOS 'skills-manifest.json')
Write-GitAttributes $RepoOS
Commit-Push $RepoOS "Sync razorblade-os from vault $stamp"

# ---- razorblade-skills (PUBLIC, tooling only) ----
Write-Host "== razorblade-skills (public) ==" -ForegroundColor Cyan
$skSk = Copy-Workflows $RepoSkills
$nSk  = New-Manifest $skSk (Join-Path $RepoSkills 'skills-manifest.json')
Write-GitAttributes $RepoSkills
$rs = @"
# razorblade-skills

Public distribution mirror of the Cowork/Obsidian OS tooling - the installable
.skill packages, their canonical workflow docs, and a SHA-256 manifest. The
Cowork sandbox pulls THIS repo over git HTTPS (no auth) to build/install skills
race-free, sidestepping the Dropbox-mount staleness (obs-014 family).

Personal brain docs are NOT here - they live in the private razorblade-os repo.
Single source of truth is the Obsidian vault; this is a one-way mirror refreshed
by WORKFLOWS/git-bridge/seed-repo.ps1.
"@
Write-Utf8NoBom (Join-Path $RepoSkills 'README.md') $rs
Commit-Push $RepoSkills "Sync razorblade-skills from vault $stamp"

Write-Host ("Done. Hashed {0} skill package(s) (os) / {1} (skills)." -f $nOS,$nSk) -ForegroundColor Green
