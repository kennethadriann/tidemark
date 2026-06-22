# TIDEMARK

A serialized sci-fi/dystopian novel, written one chapter per day by an unattended
Claude Code routine. The repo is the memory: every run reads the canon, the state,
and the last two chapters, writes the next chapter, records state forward, and
(Model B) merges to `main` only if its own self-audit passes.

## Layout
- `CLAUDE.md` — voice, pacing, workflow, self-audit (read every run)
- `bible/canon.md` — the author's-eyes-only truth + reveal map (NOT for the prose)
- `manuscript/` — front matter + one file per chapter, `_index.md` status
- `notes/state.md` — the living brain (clock, who/where, revealed, NEXT BEAT)
- `notes/recap.md` — append-only synopsis (~2 lines/chapter)
- `notes/audit.md` — weekly drift checks land here
- `.claude/commands/` — `/chapter` (daily) and `/audit` (weekly)
- `scripts/run_daily.sh` — cron entrypoint

## First-time setup
```bash
git init && git add -A && git commit -m "init: TIDEMARK through ch08"
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

## How to handle a dud
A failed self-audit leaves the chapter on a `chapter/chNN` branch instead of
`main`. Read it; either fix and merge, or delete the branch and let the next run
try again. `main` only ever gets chapters that passed.

## Notes
- `run_daily.sh` uses `--dangerously-skip-permissions` because unattended cron
  can't approve each action. Only ever point it at this repo.
- The single most important anti-drift rule: every run reads the last TWO chapters
  in full and matches their voice. Don't remove that.
