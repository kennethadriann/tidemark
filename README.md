# TIDEMARK

A serialized sci-fi/dystopian novel, written one chapter per run by an unattended
[Claude Code routine](https://code.claude.com/docs/en/claude-code-on-the-web).
The repo is the memory: every run starts cold in a fresh clone, reads the
canon, the state, and the last two chapters, writes the next chapter, records
state forward, sends the chapter to Slack, and only lets a chapter reach `main`
if its own self-audit passes.

## Layout
- `CLAUDE.md` — voice, pacing, workflow, self-audit (read every run)
- `bible/canon.md` — the author's-eyes-only truth + reveal map (NOT for the prose)
- `manuscript/` — front matter + one file per chapter, `_index.md` status
- `notes/state.md` — the living brain (clock, who/where, revealed, NEXT BEAT)
- `notes/recap.md` — append-only synopsis (~2 lines/chapter)
- `notes/audit.md` — weekly drift checks land here
- `notes/.last_run` — the audit verdict (`AUDIT: PASS` / `AUDIT: FAIL`) for the gate
- `notes/.last_commit_msg` — the commit subject the run wrote for itself
- `.claude/commands/` — `/chapter` (per run) and `/audit` (weekly)
- `scripts/run_daily.sh` — entrypoint for the alternative cron setup
- `.github/workflows/automerge.yml` — the bridge that lands passing chapters on `main`

## First-time setup
```bash
git init && git add -A && git commit -m "init: TIDEMARK"
# create an empty repo on GitHub, then:
git branch -M main
git remote add origin git@github.com:YOURNAME/tidemark.git
git push -u origin main
```

## Run it (unattended)
TIDEMARK runs as a **scheduled [Claude Code routine](https://code.claude.com/docs/en/claude-code-on-the-web)**.
A routine is a saved prompt that Claude Code runs on its own schedule, in a fresh
cloud clone of this repo, with no memory of prior runs — so the repo files are
the only state that carries forward.

Set up a routine pointed at this repo and paste the prompt below as its
instructions. Each run reconstructs state from the files, writes one chapter,
and (per CLAUDE.md) commits to a per-run `claude/...` branch that
`automerge.yml` fast-forwards onto `main`.

### Routine instructions
This is the exact prompt the routine runs each time:

```
You write TIDEMARK, a serialized novel, one chapter per run. Each run is a fresh
clone of this repo with NO memory of prior runs — the repo files are your only
memory. Follow CLAUDE.md for all voice and pacing rules (plain English, Bob Ong
style, dry humor, no AI cadence, slow burn, ONE beat per chapter, no Taglish).

STEP 1 — ORIENT. Read, in order:
- CLAUDE.md (voice + rules)
- bible/canon.md (the secret truth + REVEAL MAP — never state canon outright,
  never reveal anything ahead of the map)
- notes/state.md (clock, who/where, revealed-so-far, and the NEXT BEAT)
- notes/recap.md (running synopsis)
- the LAST TWO chapter files in manuscript/ IN FULL — match the voice to this
  real prose. This is the most important step; do not skip it.

STEP 2 — PICK the next chapter number NN from manuscript/_index.md (highest +1).

STEP 3 — GUARD. If any of these, do NOT write a chapter:
- manuscript/chNN.md already exists -> stop, do nothing.
- NEXT BEAT in state.md is missing, ambiguous, or would force a reveal ahead of
  the map -> write nothing; append a dated note to notes/audit.md saying why;
  commit that note to main; stop.

STEP 4 — WRITE manuscript/chNN.md:
- Continue from the previous chapter's exact final moment.
- Execute ONLY the NEXT BEAT. One beat. Slow. Obey the reveal map.
- Header "## Chapter NN — <Title>"; end with "*End of Chapter NN.*"; ~900-1300 words.

STEP 5 — SELF-AUDIT the draft against the checklist in CLAUDE.md (voice matches
the last 2 chapters? no staccato pile-ups / triplets / per-paragraph profundity?
exactly ONE beat? nothing revealed early? no Taglish?). If it fails, rewrite ONCE.

STEP 6 — RECORD (this is what lets tomorrow continue the story):
- Rewrite notes/state.md: advance the clock, log what you revealed this chapter,
  update who/where, and REPLACE the NEXT BEAT section with tomorrow's beat
  (one line of intent, consistent with the reveal map).
- Append ~2 lines to notes/recap.md for this chapter.
- Update manuscript/_index.md (mark NN done, add NN+1 pending).

STEP 7 — COMMIT:
- If the self-audit PASSED: commit ALL changes to the default branch (main) with
  message "ch NN: <Title>". It MUST land on main or the next run won't see it.
- If the self-audit FAILED after one rewrite: commit to a branch named
  claude/review-chNN instead, and stop — leave main clean for human review.

Write at most ONE chapter per run. Touch nothing outside this repo.

send the new chapter to slack channel using the webhook
```

The routine also delivers each new chapter to a Slack channel via an
[incoming webhook](https://api.slack.com/messaging/webhooks) (its URL is kept
out of the repo and passed in the routine prompt).

### Alternative: local cron
If you'd rather run it on your own machine instead of the hosted routine, use
`scripts/run_daily.sh` from crontab (`crontab -e`):
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

- **Claude Code routine + GitHub Actions (`automerge.yml`).** The run happens on
  a `claude/**` branch (the harness won't let it push to `main`), so
  `automerge.yml` is the bridge: it fast-forwards `main` for a passing run, and
  refuses to merge anything on a `claude/review-*` branch or any push whose
  `notes/.last_run` says `AUDIT: FAIL`.
- **Local cron (`run_daily.sh`).** The run works on a `chapter/chNN` branch. On
  `AUDIT: PASS` it merges to `main` and pushes; on `AUDIT: FAIL` it pushes the
  branch to origin for review and leaves `main` alone.

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
