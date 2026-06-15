<#
  rotate-changelog.ps1  -  Desktop-side _CHANGELOG rotation (the carve log-rotate gates).

  Why DESKTOP, not sandbox: writing a large file into the Dropbox vault is SAFE from
  the desktop (an ordinary local write Dropbox then syncs). The Cowork sandbox sees a
  STALE, TRUNCATED partial of large cloud files (obs-014 / obs-084), so it can neither
  measure nor carve _CHANGELOG safely - it only measure-and-gates. The carve is a
  desktop-owned write (obs-083: scope the hazard to the context that owns it). The
  Git Bridge (razorblade-os) is the byte-exact restore floor if anything looks wrong.

  What it does: keeps the most-recent N distinct dates of entries live (default 2),
  carves everything older VERBATIM into SYSTEM\history\_CHANGELOG-<bucket>.md, normalizes the
  live file to clean newest-first order (also fixing any foot-append inversion), and
  leaves a foot pointer. Append-only history is preserved - nothing is deleted, only
  moved. Integrity is asserted (every entry lands in exactly one file, no body lost)
  BEFORE anything is written.

  SAFE BY DEFAULT: prints the plan and writes nothing. Add -Execute to apply.

  Usage (run on the DESKTOP):
    # preview only:
    powershell -ExecutionPolicy Bypass -File "C:\Users\Chad\Dropbox\razorblade_mermaid\WORKFLOWS\git-bridge\rotate-changelog.ps1"
    # apply:
    powershell -ExecutionPolicy Bypass -File "...\rotate-changelog.ps1" -Execute
    # keep more/less history live, or force a bucket name:
    powershell ... -KeepDates 3 -Execute
#>
param(
  [int]    $KeepDates = 2,
  [string] $Bucket    = '2026-H1',
  [switch] $Execute
)

$ErrorActionPreference = 'Stop'

$Vault      = 'C:\Users\Chad\Dropbox\razorblade_mermaid'
$ClPath     = Join-Path $Vault '_CHANGELOG.md'
$HistDir    = Join-Path $Vault 'SYSTEM\history'
$ArcPath    = Join-Path $HistDir ("_CHANGELOG-$Bucket.md")
$ArcLink    = "SYSTEM/history/_CHANGELOG-$Bucket"
$Log        = Join-Path $Vault 'WORKFLOWS\git-bridge\sync.log'
$Today      = Get-Date -Format 'yyyy-MM-dd'
$EntryRe    = '^## \d{4}-\d{2}-\d{2}'   # a real changelog entry heading (NOT "## Entry format" / fenced "## YYYY-MM-DD")

function Write-Utf8NoBom($path, $text) {
  [System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))
}
function Fail($msg) {
  "$(Get-Date -Format 'o')  ROTATE ERROR  $msg" | Add-Content $Log
  throw $msg
}

if (-not (Test-Path $ClPath)) { Fail "changelog not found: $ClPath" }

# ---- read (desktop = authoritative; normalize newlines to LF for processing) ----
$raw    = [System.IO.File]::ReadAllText($ClPath)
$origLen= $raw.Length
$lines  = ($raw -replace "`r`n","`n") -split "`n"

# ---- locate the structural header ----
$idxCl = -1
for ($k=0; $k -lt $lines.Count; $k++) { if ($lines[$k] -match '^#\s+CHANGELOG\s*$') { $idxCl = $k; break } }
if ($idxCl -lt 0) { Fail "no '# CHANGELOG' heading found" }
$frontmatter = if ($idxCl -gt 0) { ($lines[0..($idxCl-1)] -join "`n") } else { '' }
$bodyStart   = $idxCl + 1
$body        = $lines[$bodyStart..($lines.Count-1)]

# ---- single pass: fence-aware classification of each body line ----
$n = $body.Count
$isEntry = New-Object bool[] $n
$inFence = $false
for ($i=0; $i -lt $n; $i++) {
  $ln = $body[$i]
  if ($ln -match '^\s*```') { $inFence = -not $inFence; continue }
  if (-not $inFence -and $ln -match $EntryRe) { $isEntry[$i] = $true }
}

# preamble block = the "> For any AI..." note through the next real entry (incl. ## Entry format + fence)
$preStart = -1
for ($i=0; $i -lt $n; $i++) { if ($body[$i] -match '^>\s' ) { $preStart = $i; break } }
$preEnd = -1
if ($preStart -ge 0) {
  $preEnd = $n - 1
  for ($i=$preStart+1; $i -lt $n; $i++) { if ($isEntry[$i]) { $preEnd = $i-1; break } }
}
$preamble = if ($preStart -ge 0) { ($body[$preStart..$preEnd] -join "`n").Trim("`n") } else { '' }

# ---- collect entries (skipping the preamble range), each = heading line .. next boundary ----
$entries = New-Object System.Collections.ArrayList
$i = 0
while ($i -lt $n) {
  if ($preStart -ge 0 -and $i -ge $preStart -and $i -le $preEnd) { $i = $preEnd + 1; continue }
  if ($isEntry[$i]) {
    $start = $i
    $j = $i + 1
    while ($j -lt $n) {
      if ($preStart -ge 0 -and $j -eq $preStart) { break }   # preamble is a hard boundary
      if ($isEntry[$j]) { break }
      $j++
    }
    $text = ($body[$start..($j-1)] -join "`n").TrimEnd("`n")
    $date = ($body[$start] -replace '^## (\d{4}-\d{2}-\d{2}).*','$1')
    [void]$entries.Add([pscustomobject]@{ Date=$date; Heading=$body[$start]; Text=$text; Idx=$entries.Count })
    $i = $j
  } else { $i++ }
}
if ($entries.Count -eq 0) { Fail "parsed 0 entries - aborting rather than risk a malformed carve" }

# ---- decide keep vs carve by most-recent N distinct dates (whole date-groups) ----
$distinct = $entries.Date | Sort-Object -Descending -Unique
$keepDatesSet = @($distinct | Select-Object -First $KeepDates)
$cutoff = $keepDatesSet[-1]
$keep  = @($entries | Where-Object { $_.Date -ge $cutoff })
$carve = @($entries | Where-Object { $_.Date -lt $cutoff })

# newest-first, stable within a date (Idx ascending = original order preserved)
$keepSorted  = @($keep  | Sort-Object @{e={$_.Date};desc=$true}, @{e={$_.Idx};desc=$false})
$carveSorted = @($carve | Sort-Object @{e={$_.Date};desc=$true}, @{e={$_.Idx};desc=$false})

# ---- integrity asserts (BEFORE any write) ----
if (($keep.Count + $carve.Count) -ne $entries.Count) { Fail "keep+carve != total ($($keep.Count)+$($carve.Count) vs $($entries.Count))" }
$allHead  = ($entries     | ForEach-Object Heading) | Sort-Object
$splitHead= (($keepSorted + $carveSorted) | ForEach-Object Heading) | Sort-Object
if (Compare-Object $allHead $splitHead) { Fail "entry headings not conserved across split" }
$origBodyChars  = ($entries     | ForEach-Object { $_.Text.Length } | Measure-Object -Sum).Sum
$splitBodyChars = (($keepSorted + $carveSorted) | ForEach-Object { $_.Text.Length } | Measure-Object -Sum).Sum
if ($origBodyChars -ne $splitBodyChars) { Fail "entry body chars not conserved ($origBodyChars vs $splitBodyChars)" }

# ---- assemble outputs ----
$pointer = "> Entries dated before $cutoff archived to [[$ArcLink]] (rotated $Today)."
$liveParts = @()
if ($frontmatter) { $liveParts += $frontmatter }
$liveParts += "# CHANGELOG"
if ($preamble)    { $liveParts += $preamble }
$liveParts += (($keepSorted | ForEach-Object { $_.Text }) -join "`n`n")
$liveParts += $pointer
$liveText = ($liveParts -join "`n`n").TrimEnd("`n") + "`n"

$arcHeader = @"
---
type: ai-os-archive
file: changelog-archive
purpose: Rotated _CHANGELOG entries (older history). Verbatim; newest-first.
rotated_from: _CHANGELOG.md
last_updated: $Today
---

# CHANGELOG - ARCHIVE $Bucket

> Rotated out of [[_CHANGELOG]] on $Today by rotate-changelog.ps1. Verbatim entries; the live log is [[_CHANGELOG]].
"@
$carveBody = ($carveSorted | ForEach-Object { $_.Text }) -join "`n`n"

# carve nothing? then it's already lean enough for the chosen KeepDates - no-op.
if ($carve.Count -eq 0) {
  Write-Host "Nothing older than the most-recent $KeepDates date(s) - changelog already lean. No-op." -ForegroundColor Yellow
  "$(Get-Date -Format 'o')  ROTATE  no-op (keepDates=$KeepDates, entries=$($entries.Count))" | Add-Content $Log
  return
}

# ---- report ----
$liveBytes = ([Text.Encoding]::UTF8.GetByteCount($liveText))
Write-Host "rotate-changelog plan:" -ForegroundColor Cyan
Write-Host ("  entries parsed : {0}  (dates {1} .. {2})" -f $entries.Count, $distinct[-1], $distinct[0])
Write-Host ("  keep (live)    : {0} entries, dates >= {1}  ->  ~{2:N0} bytes" -f $keep.Count, $cutoff, $liveBytes)
Write-Host ("  carve (archive): {0} entries, dates <  {1}  ->  {2}" -f $carve.Count, $cutoff, $ArcPath)
Write-Host ("  newest carved  : {0}" -f $carveSorted[0].Heading)
Write-Host ("  oldest carved  : {0}" -f $carveSorted[-1].Heading)
Write-Host ("  original size  : {0:N0} bytes" -f $origLen)

if (-not $Execute) {
  Write-Host "DRY RUN - nothing written. Re-run with -Execute to apply." -ForegroundColor Yellow
  return
}

# ---- stage to temp, verify, then commit to disk ----
New-Item -ItemType Directory -Force -Path $HistDir | Out-Null
$tmpLive = [IO.Path]::GetTempFileName()
$tmpArc  = [IO.Path]::GetTempFileName()
Write-Utf8NoBom $tmpLive $liveText

if (Test-Path $ArcPath) {
  # prepend the new (newer) carve block after the existing archive header
  $exist = [IO.File]::ReadAllText($ArcPath)
  $marker = "by rotate-changelog.ps1"
  $hdrCut = $exist.IndexOf($marker)
  if ($hdrCut -lt 0) { Fail "existing archive $ArcPath has an unexpected shape - resolve by hand" }
  $hdrEnd = $exist.IndexOf("`n", $hdrCut)
  $head   = $exist.Substring(0, $hdrEnd)
  $rest   = $exist.Substring($hdrEnd)
  Write-Utf8NoBom $tmpArc ($head + "`n`n" + $carveBody + "`n" + $rest)
} else {
  Write-Utf8NoBom $tmpArc ($arcHeader + "`n`n" + $carveBody + "`n")
}

# post-write sanity: live shrank, archive non-trivial, both parse-readable
$newLiveLen = (Get-Item $tmpLive).Length
$newArcLen  = (Get-Item $tmpArc).Length
if ($newLiveLen -ge $origLen) { Remove-Item $tmpLive,$tmpArc -Force; Fail "staged live ($newLiveLen) not smaller than original ($origLen)" }
if ($newArcLen  -lt 200)      { Remove-Item $tmpLive,$tmpArc -Force; Fail "staged archive suspiciously small ($newArcLen bytes)" }

Move-Item $tmpArc  $ArcPath -Force
Move-Item $tmpLive $ClPath  -Force

Write-Host ("DONE. live {0:N0} -> {1:N0} bytes; archived {2} entries to {3}." -f $origLen, $newLiveLen, $carve.Count, $ArcPath) -ForegroundColor Green
Write-Host "Run seed-repo.ps1 (or wait for the scheduled sync) to commit the rotation to GitHub." -ForegroundColor Cyan
("{0}  ROTATE  live={1}->{2}B  carved={3} -> {4}" -f (Get-Date -Format 'o'), $origLen, $newLiveLen, $carve.Count, ("_CHANGELOG-$Bucket.md")) | Add-Content $Log
