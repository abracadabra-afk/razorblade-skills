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
$Log        = Join-Path $Vault 'WORKFLOWS\git-bridge\sync.log'

# unattended-run visibility: log any terminating error instead of failing silently
trap { "$(Get-Date -Format 'o')  ERROR  $($_.Exception.Message)" | Add-Content $Log; break }

# Preflight: git MUST be on PATH (^obs-100). The scheduled task has run in a shell
# where git was absent, turning the push into a logged-but-late failure part-way
# through a two-repo sync (os pushed, skills not, or neither). Fail early + clearly,
# before any repo work, so sync.log carries an actionable message instead of a raw
# "git is not recognized" from mid-Commit-Push.
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "git not found on PATH - install git or add it to the scheduled task's PATH before running seed-repo.ps1 (^obs-100)"
}

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
  # skills-src/ : the editable text source for the packages (diffable in git; pack-skills.ps1 builds .skill from it)
  $srcSrc = Join-Path $wfSrc 'skills-src'
  if (Test-Path $srcSrc) {
    $srcDst = Join-Path $wfDst 'skills-src'
    if (Test-Path $srcDst) { Remove-Item $srcDst -Recurse -Force }
    Copy-Item $srcSrc $srcDst -Recurse -Force
  }
  # Git Bridge tooling (build.py + the desktop scripts) so the sandbox pulls them with the repo
  $gSrc = Join-Path $wfSrc 'git-bridge'
  if (Test-Path $gSrc) {
    $gDst = Join-Path $wfDst 'git-bridge'
    New-Item -ItemType Directory -Force -Path $gDst | Out-Null
    foreach ($t in 'build.py','seed-repo.ps1','setup-schedule.ps1','pack-skills.ps1','rotate-changelog.ps1') {
      $tp = Join-Path $gSrc $t
      if (Test-Path $tp) { Copy-Item $tp $gDst -Force }
    }
  }
  return (Join-Path $wfDst 'skills')
}

# content_sha256 == build.py's recipe over the PACKAGE's files (relpaths stripped of the
# leading <name>/), so it equals build.py's manifest value and is exactly what
# `build.py audit` recomputes from the package. Lets the spec'd SOURCE-AHEAD check
# (compare source content-hash to the manifest's content_sha256) run against this manifest.
function Get-PackageContentSha($skillPath) {
  Add-Type -AssemblyName System.IO.Compression.FileSystem -ErrorAction SilentlyContinue
  $name = [System.IO.Path]::GetFileNameWithoutExtension($skillPath)
  $zip  = [System.IO.Compression.ZipFile]::OpenRead($skillPath)
  try {
    $entries = @{}
    foreach ($e in $zip.Entries) {
      if ($e.FullName.EndsWith('/')) { continue }                 # skip directory entries
      $rel = $e.FullName.Replace('\','/')   # normalize Windows backslash zip entries (^obs-092)
      if ($rel.StartsWith("$name/")) { $rel = $rel.Substring($name.Length + 1) }
      $s   = $e.Open()
      $msf = New-Object System.IO.MemoryStream
      $s.CopyTo($msf); $s.Close()
      $entries[$rel] = $msf.ToArray()
    }
    $sha  = [System.Security.Cryptography.SHA256]::Create()
    $ms   = New-Object System.IO.MemoryStream
    $keys = [string[]]@($entries.Keys)
    [Array]::Sort($keys, [System.StringComparer]::Ordinal)   # ORDINAL (codepoint) to match Python's sorted() in build.py; default Sort-Object is culture/case-insensitive and reorders 'SKILL.md' vs lowercase paths
    foreach ($rel in $keys) {
      $rb = [Text.Encoding]::UTF8.GetBytes($rel)
      $ms.Write($rb, 0, $rb.Length); $ms.WriteByte(0)
      $fh = $sha.ComputeHash($entries[$rel])
      $ms.Write($fh, 0, $fh.Length)
    }
    -join ($sha.ComputeHash($ms.ToArray()) | ForEach-Object { $_.ToString('x2') })
  } finally { $zip.Dispose() }
}

function New-Manifest($skillsDir, $outFile) {
  $skills = @()
  if (Test-Path $skillsDir) {
    Get-ChildItem $skillsDir -Filter *.skill | Sort-Object Name | ForEach-Object {
      $skills += [ordered]@{
        name           = $_.BaseName
        package        = "WORKFLOWS/skills/$($_.Name)"
        sha256         = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower()
        content_sha256 = (Get-PackageContentSha $_.FullName)
        bytes          = $_.Length
      }
    }
  }
  $m = [ordered]@{
    generated = (Get-Date -Format 'o')
    note      = 'sha256 = zip hash of each built .skill package; content_sha256 = build.py-recipe hash over the package contents (SKILL.md+assets, installed-comparable). skill-audit / build.py audit compare installed-vs-this.'
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

# Build any changed skills from their text source first (source -> package), so the sync ships them.
# Change-detected: no source change = no-op. This is what makes the daily task close the whole loop.
$packScript = Join-Path $Vault 'WORKFLOWS\git-bridge\pack-skills.ps1'
if (Test-Path $packScript) {
  try { & $packScript | Out-Host }
  catch { Write-Warning ("pack-skills failed: " + $_.Exception.Message + " - continuing with the sync") }
}

# Non-destructive housekeeping reminder: nudge when the append-only changelog gets large.
# The carve itself stays a deliberate, reviewed desktop action (rotate-changelog.ps1 dry-run -> eyeball -> -Execute);
# it is NEVER auto-run here - this only tells you WHEN it is due.
$ChangelogReminderKB = 200
$clog = Join-Path $Vault '_CHANGELOG.md'
if (Test-Path $clog) {
  $clogKB = [math]::Round((Get-Item $clog).Length / 1KB)
  if ($clogKB -ge $ChangelogReminderKB) {
    Write-Warning ("_CHANGELOG.md is {0} KB (>= {1}) - time to rotate: run WORKFLOWS\git-bridge\rotate-changelog.ps1 (dry-run), eyeball, then -Execute." -f $clogKB, $ChangelogReminderKB)
    ("{0}  REMIND  _CHANGELOG.md {1}KB >= {2}KB - run rotate-changelog.ps1" -f (Get-Date -Format 'o'), $clogKB, $ChangelogReminderKB) | Add-Content $Log
  }
}

# ---- brain-doc size stamp (^backlog-logrotate-exact-size / ^obs-090) ----
# The sandbox's log-rotate pass cannot size the brain docs byte-exactly: the file tools
# expose only line/token counts and bash `wc -c` on the mount serves stale partials
# (^obs-084). This desktop run has authoritative file access, so it stamps byte-exact
# sizes for every brain doc into SYSTEM/reports/brain-doc-sizes.json on each daily sync.
# log-rotate Step 1 reads the stamp (if fresh) instead of the token->char proxy.
# Serialized via ConvertTo-Json (DIR-004 discipline); wrapped so it can never break the sync.
try {
  $sizes = [ordered]@{
    generated = (Get-Date -Format 'o')
    source    = 'seed-repo.ps1 (desktop, authoritative filesystem)'
    note      = 'bytes = UTF-8 file length; >= char count, so banding on bytes errs toward rotating early (safe). Written every daily Git Bridge sync.'
    files     = [ordered]@{}
  }
  foreach ($f in $brain) {
    $src = Join-Path $Vault $f
    if (Test-Path $src) { $sizes.files[$f] = (Get-Item $src).Length }
  }
  # per-project backlog shards (in log-rotate's measured set since 2026-06-29)
  Get-ChildItem (Join-Path $Vault 'WRITING\PROJECTS\*\backlog.md') -ErrorAction SilentlyContinue | ForEach-Object {
    $rel = $_.FullName.Substring($Vault.Length + 1).Replace('\','/')
    $sizes.files[$rel] = $_.Length
  }
  $reportsDir = Join-Path $Vault 'SYSTEM\reports'
  New-Item -ItemType Directory -Force -Path $reportsDir | Out-Null
  Write-Utf8NoBom (Join-Path $reportsDir 'brain-doc-sizes.json') ($sizes | ConvertTo-Json -Depth 4)
} catch {
  Write-Warning ("brain-doc size stamp failed: " + $_.Exception.Message + " - continuing with the sync")
}

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
"$(Get-Date -Format 'o')  OK  os=$nOS skills=$nSk" | Add-Content $Log
