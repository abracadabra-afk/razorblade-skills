# razorblade-skills

Public distribution mirror of the Cowork/Obsidian OS tooling - the installable
.skill packages, their canonical workflow docs, and a SHA-256 manifest. The
Cowork sandbox pulls THIS repo over git HTTPS (no auth) to build/install skills
race-free, sidestepping the Dropbox-mount staleness (obs-014 family).

Personal brain docs are NOT here - they live in the private razorblade-os repo.
Single source of truth is the Obsidian vault; this is a one-way mirror refreshed
by WORKFLOWS/git-bridge/seed-repo.ps1.