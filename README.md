# TIDEMARK

A serialized sci-fi/dystopian novel, written one chapter per run by an unattended
Claude Code routine. The repo is the memory: every run starts cold, reads the
canon, the state, and the last two chapters, writes the next chapter, records
state forward, and only lets a chapter reach `main` if its own self-audit passes.

## Layout
- `CLAUDE.md` — voice, pacing, workflow, self-audit (read every run)
- `bible/canon.md` — the author's-eyes-only truth + reveal map (NOT for the prose)
- `manuscript/` — front matter + one file per chapter, `_index.md` status
- `notes/state.md` — the living brain (clock, who/where, revealed, NEXT BEAT)
- `notes/recap.md` — append-only synopsis (~2 lines/chapter)
- `notes/audit.md` — weekly drift checks land here
- `notes/.last_run` — the audit verdict (`AUDIT: PASS` / `AUDIT: FAIL`) for the gate
- `notes/.last_commit_msg` — the commit subject the run wrote for itself
- `.claude/commands/` — `/chapter` (daily) and `/audit` (weekly)
- `scripts/run_daily.sh` — cron entrypoint
- `.github/workflows/automerge.yml` — the bridge that lands passing chapters on `main`

## First-time setup
```bash
git init && git add -A && git commit -m "init: TIDEMARK"
# create an empty repo on GitHub, then:
git branch -M main
git remote add origin git@github.com:YOURNAME/tidemark.git
git push -u origin main
```

## Run it daily (unattended)
Edit your crontab (`crontab -e`):
```
0 6 * * *  TIDEMARK_DIR=$HOME/tidemark /bin/bash $HOME/tidemark/scripts/run_daily.sh >> $HOME/tidemark/notes/cron.log 2>&1
```
`run_daily.sh` figures out the next chapter number from `manuscript/`, runs
`/audit` on every 7th chapter (and `/chapter` otherwise), and writes the draft
on its own branch before deciding whether it earns `main`.

## How a chapter reaches `main`
A run never writes straight to `main`. It works on a branch and leaves an audit
verdict in `notes/.last_run`. There are two ways that branch lands on `main`,
and the repo supports both:

- **Local cron (`run_daily.sh`).** The run works on a `chapter/chNN` branch. On
  `AUDIT: PASS` it merges to `main` and pushes; on `AUDIT: FAIL` it pushes the
  branch to origin for review and leaves `main` alone.
- **Hosted harness + GitHub Actions (`automerge.yml`).** When the run happens on
  a `claude/**` branch (the harness won't let it push to `main`),
  `automerge.yml` is the bridge: it fast-forwards `main` for a passing run, and
  refuses to merge anything on a `claude/review-*` branch or any push whose
  `notes/.last_run` says `AUDIT: FAIL`.

Either way, `main` only ever gets chapters that passed.

## How to handle a dud
A failed self-audit leaves the chapter quarantined on a branch instead of `main`
— `chapter/chNN` under the cron model, `claude/review-chNN` under the hosted
model. Read it; either fix and merge, or delete the branch and let the next run
try again.

## Notes
- `run_daily.sh` uses `--dangerously-skip-permissions` because unattended cron
  can't approve each action. Only ever point it at this repo.
- The single most important anti-drift rule: every run reads the last TWO chapters
  in full and matches their voice. Don't remove that.
