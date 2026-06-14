---
type: proposal
name: git-bridge
status: proposed
lane: meta / os
last_updated: 2026-06-14
decision: scope ruled HYBRID (CRE, 2026-06-14); awaiting repo creation to build
supersedes_candidate: graduates the file-tools-only posture (^obs-014 family) and ^patch-tool-hygiene
---

# Git Bridge — a versioned source of truth for skills + brain docs

> **Status:** Architecture proposed and scope ruled. CRE chose the **hybrid** split (2026-06-14). Build is staged below; steps 3–5 are mine to execute once the repo exists. Steps 1–2 are CRE's (auth boundary).

## The problem (why the Dropbox mount keeps costing reconfirmation time)

CRE's recurring complaint — constantly re-confirming and re-reviewing already-completed work because the information is fragile and often wrong — traces in `_OBSERVATIONS` to **three distinct failure classes**, not one:

1. **Bash-mount staleness / truncation / phantom NULs / EACCES** — the `^obs-014` family (obs-014, 031–035, 039, 040, 042, 054, 058, 060). Root cause confirmed this session from the sandbox `mount` table: bash reads the vault through a `virtiofs → Windows → Dropbox-FUSE` chain that races the cloud sync, while the file tools read the cloud-true copy by a different path. This is the truncated-`scaffold_ingest.py`-every-ingest problem.
2. **No version history / no restore floor** — `^obs-060` / `^obs-062`. Dropbox-only, no git repo, no git plugin. When `_SKILLS MAP` truncated, the only point-in-time backup was Dropbox's web history, which the sandbox can't reach — so restores had to be hand-reconstructed from sibling docs.
3. **Skill staleness + repetitive reinstalls** — the entire `^backlog-*-rebuild` / `reinstall` pile. Three layers (canonical doc → `.skill` package → installed copy in app-data); the installed copy that actually *runs* constantly lags, with no reliable "is this current?" signal, so currency gets reconfirmed by hand.

## The enabling finding (verified 2026-06-14)

Probed network reachability from the Cowork bash sandbox (same method as `^obs-059`):

| Target | Result | Implication |
|---|---|---|
| `git ls-remote https://github.com/...` | **returned a real HEAD SHA** | git smart-HTTP clone/fetch/pull/**push** work |
| `github.com` (HTTPS) | **200** | reachable |
| `api.github.com` | `000` | GitHub REST API is **blocked** |
| `raw.githubusercontent.com` | `000` | raw-file URLs **blocked** |
| `codeload.github.com` | `000` | tarball/zip download **blocked** |
| `gitlab.com` | `000` | GitLab **blocked** — GitHub specifically is allowlisted |
| `pypi.org` | 200 (control) | unchanged |
| `huggingface.co` | `000` (control) | unchanged (`^obs-059`) |

**Conclusion:** the core git transport on `github.com` is on the sandbox allowlist even though the GitHub API and raw/tarball paths are not. That is exactly enough — the plan must use **git transport only** (clone / fetch / pull / push), never the REST API or `raw`/`codeload` URLs.

## How git maps onto each problem

- **Problem 2 (history): fully fixed.** Real diffs, atomic commits, instant restore of any truncated file. Retires `^obs-060` / `^obs-062`.
- **Problem 3 (skill currency): mostly fixed.** Versioned `.skill` packages make "is it current?" a SHA comparison (which `skill-audit` already wants); rebuilds become reproducible. The one piece git can't reach is the last-mile Cowork **"Save skill"** into app-data — that stays a manual click, but a rare, deterministic one (only when a SHA actually changed) instead of guessing.
- **Problem 1 (bash-mount race): partially fixed — the subtle part.** Git does **not** fix stale reads of files that still live under the Dropbox mount. **But** building skills by `git clone`ing the GitHub remote into the sandbox's own `/tmp` (not the Dropbox mount) reads a clean, race-free, sandbox-local copy — which kills the truncated-scaffolder recurrence (`^obs-031`/`034`/`035`) at the source. Git fixes the **build/install path**; live prose-vault reads still need the file-tools-only discipline.

## Decision: HYBRID split (ruled 2026-06-14)

**In the git repo** (GitHub, private):
- Brain docs: `_ME`, `_VAULT MAP`, `_SKILLS MAP`, `_DIRECTIVES`, `_OBSERVATIONS`, `_BACKLOG`, `_CHANGELOG`.
- Skill canon: `WORKFLOWS/*.md`.
- Build scripts + the built `.skill` packages (`WORKFLOWS/skills/`).
- A `skills-manifest.json` mapping each skill's three layers (doc → package → expected installed SHA).

**Stays on Dropbox** (deliberately out of git):
- Fiction prose (`WRITING/`) and the dictation inbox — because the dictation-runner (`^obs-059`) uses **Dropbox as the phone-audio transport**, and the vendored 484 MB whisper model would wreck a git tree without LFS.

Rationale: hybrid fixes the two classes that cost the most reconfirmation time (skill currency + brain-doc truncation/history) and the build-path race, while keeping the phone-dictation pipeline and large binaries on the transport that suits them. Smallest blast radius.

## Roles

- **Desktop = the writer (push side).** CRE's machine has full internet. Obsidian-Git plugin or plain git commits/pushes. This is what finally gives the restore floor `^obs-062` said didn't exist. The push credential (PAT) lives **only** in the desktop OS credential store — never in the vault or agent context (DIR-001).
- **Cowork = the reader/builder (pull side).** Skill builds `git clone --depth 1` into the sandbox, build deterministically there, hand the package to "Save skill." Pull needs no auth.

## Staged build

**CRE only (auth boundary):**
1. Create an empty **private** GitHub repo (suggested name `inkwell-os` or `razorblade-os`).
2. Configure desktop git/Obsidian-Git with a PAT in the OS credential store. Sandbox only ever pulls.

**Mine to execute once the repo exists:**
3. **Scaffold repo contents** in a staging dir: directory layout, `skills-manifest.json`, deterministic `build.py`, `SYNC.md` runbook. This is the clean home for the half-built `skills-manager` / registry work (`^skills-manager-build`, `^obs-056`).
4. **Seed** with current canonical files + the healthy `.skill` packages, so the first push is a known-good baseline — and the truncated `_SKILLS MAP` tail plus the `register-pass` / `transcoder` / `chapter-init` rebuilds get rebuilt **once**, from a race-free clone, then never drift silently again.
5. **Rewire `skill-audit`** to do the SHA comparison (installed vs repo) instead of the stale-mount inspection that throws `^obs-014` false positives — the piece that ends the "did I already install this?" loop.

## Standing flow once live

Desktop pushes → history + restore floor (retires `^obs-060`/`062`). Cowork pulls into `/tmp` and builds race-free (retires `^obs-031`/`034`/`035`). `skill-audit` reports currency by SHA. CRE "Save skill" only when a SHA actually changed.

## Honest caveats / non-goals

- **Does not** make bash reads of the prose vault on Dropbox reliable — that race stays. The fix for that lane remains the **file-tools-only discipline**, which this proposal recommends graduating from candidate (`^obs-014`/`032`/`058`, `^patch-tool-hygiene`) to a real `_DIRECTIVES` rule.
- **Does not** eliminate the manual Cowork "Save skill" click — only makes it deterministic and rare. (Open question worth checking later: whether Cowork can install a skill from a path/manifest without the UI click.)
- Uses **git transport only**; any future step that reaches for the GitHub API, `raw.githubusercontent`, or release tarballs will fail in the sandbox (all `000`).

## References

`^obs-014` · `^obs-031`/`034`/`035` · `^obs-058` · `^obs-059` · `^obs-060` · `^obs-062` · `^skills-manager-build` · `^patch-tool-hygiene` · backlog `^git-bridge-build`.
