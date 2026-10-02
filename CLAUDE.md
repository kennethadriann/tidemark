# TIDEMARK — writing instructions (read this every run)

You are writing a serialized sci-fi/dystopian novel, one chapter per run.
The repo is the memory. You start cold every run; reconstruct state from files.

## VOICE (non-negotiable)
- First person, past tense, narrator = Adz.
- Plain English. Bob Ong style: short sentences, dry humor, conversational,
  grounded, easy for people who don't read much.
- THE VOICE IS CHAPTERS 1 AND 6. Not the last chapter. Every run you re-read
  manuscript/ch01.md and manuscript/ch06.md as the permanent voice anchor.
  If your draft sounds closer to the recent chapters than to Ch1/Ch6, the
  recent chapters drifted. Pull back toward Ch1/Ch6.
- Adz is a modern data guy from a tower. He jokes. He thinks in tickets,
  scripts, rows, datasets, numbers. He talks to the reader ("Here's what I
  do."). He is NOT a frontier drifter. Banned folksy/archaic register:
  "a good many," "no crime in it," "I'd reckon," "fool's care," "set it down
  like a load," "I didn't much care for," long "and... and... and" chains.
- Paragraphs mostly short to medium. A long paragraph is the exception.
- At least TWO dry jokes per chapter, the kind Ch1 has.
- DIALOGUE: most chapters have people talking. Never more than TWO chapters
  in a row with zero dialogue. People are the story; scenery is not.
- NO Taglish in the prose. (Filipino names and food are fine and good.)
- NO "AI cadence." Specifically avoid:
  - the "Short. Punchy. Dramatic." staccato one-line-paragraph pile-up
  - rule-of-three triplets ("smart, precise, and allergic to...")
  - a profound "button" line at the end of every paragraph
  - em-dash overuse (a few per chapter is fine, like Ch1; zero is not the goal)
  - every sentence reaching for meaning. Let plain things stay plain.

## PACING (non-negotiable)
- One chapter = ONE beat, and the beat must CHANGE something: new information,
  a new place, a person arriving or leaving, a decision made, a reveal landed.
  "He walked further and noticed a fresh small feeling" is NOT a beat.
- Travel and routine get COMPRESSED. Skip days in a sentence. Never spend a
  chapter on a leg of a journey unless something happens on it.
- Obey the STORY PLAN in bible/canon.md. Each milestone has a "no later than"
  chapter. If the current chapter is at or past a milestone's deadline, this
  chapter's beat MUST be that milestone. Being behind the plan is a failure,
  same as revealing ahead of the map.
- Quiet endings are good. Not every chapter needs a cliffhanger, but the book
  must keep moving toward the core.
- Chapter length: ~900–1300 words.
- CLOCKS ARE REAL. Track in-story time in notes/state.md. Never freeze a
  deadline or tell yourself "don't mention the number." If a date passes,
  that is story, and it goes on the page.

## BEFORE WRITING — orient (always, in this order)
1. Read bible/canon.md — the secret truth, the REVEAL MAP, and the STORY PLAN.
   Never state canon outright. Never reveal anything ahead of its milestone.
2. Read notes/state.md — the clock, who/where, revealed-so-far, NEXT BEAT.
3. Read notes/recap.md — the running synopsis.
4. Read manuscript/ch01.md and manuscript/ch06.md — the VOICE ANCHOR.
5. Read the LAST TWO chapter files in manuscript/ IN FULL — for continuity
   (where everyone is, the exact last moment). Match the VOICE to Ch1/Ch6,
   not to these.

## GUARD — before you write
- If manuscript/ already has a file for today's chapter number: STOP, write nothing.
- If NEXT BEAT is missing, ambiguous, or would force a reveal ahead of the map:
  WRITE NOTHING. Append a note to notes/audit.md explaining why, and exit.
  A skipped day is fine. A wrong chapter on main is not.

## WRITE
- Continue from the previous chapter's final moment (a time skip is allowed
  if the NEXT BEAT calls for one; say it plainly, Ch1-style).
- Execute ONLY the NEXT BEAT. Obey the reveal map and the story plan.
- Title the chapter "## Chapter NN — <Title>". End with "*End of Chapter NN.*".

## SELF-AUDIT — before saving, re-read your own draft against this checklist
- [ ] Does it sound like Ch1/Ch6 (jokes, modern, short paragraphs), not like
      the recent chapters?
- [ ] No banned folksy register, no staccato pile-ups, no triplets, no
      per-paragraph profundity?
- [ ] Did the beat CHANGE something? Could you say what in one sentence?
- [ ] On or ahead of the STORY PLAN deadline? Nothing revealed ahead of the map?
- [ ] Dialogue present (or this isn't the third silent chapter in a row)?
- [ ] No Taglish in prose?
If ANY box fails: rewrite ONCE. If it still fails, write "AUDIT: FAIL" to
notes/.last_run (otherwise write "AUDIT: PASS") and still save the draft — the
git wrapper will quarantine it on its branch instead of merging to main.

## AFTER WRITING — record (this is what makes tomorrow flow)
1. Save manuscript/chNN.md.
2. REWRITE notes/state.md using its existing headings. HARD CAP ~4 KB.
   - CLOCK: in-story days since Ch1, plus every live deadline and whether it
     has passed.
   - WHO/WHERE: one line per character that matters.
   - REVEALED SO FAR: short bullets of what the READER now knows. Do not log
     per-chapter history here; that's what recap.md is for.
   - PLAN POSITION: which milestone is next and its deadline chapter.
   - NEXT BEAT: one concrete event for tomorrow that changes something.
   - AVOID: at most 8 bullets. Drop old ones when you add new ones.
3. Append ~2 lines to notes/recap.md for this chapter.
4. Update manuscript/_index.md (mark NN done, add NN+1 pending).
5. Write the commit message to notes/.last_commit_msg as:  ch NN: <Title>
6. Write "AUDIT: PASS" or "AUDIT: FAIL" to notes/.last_run.

## HOW COMMITS REACH MAIN (don't panic about the branch)
- You run on a per-run `claude/...` branch; the harness will NOT let you push
  straight to `main`. That's expected. Just commit your work and push your
  branch — do NOT try to force a push to `main`.
- A GitHub Actions workflow (.github/workflows/automerge.yml) is the bridge:
  - PASS run on a normal `claude/...` branch -> it fast-forwards `main` for you.
  - FAIL run committed to `claude/review-chNN` -> it leaves it quarantined,
    never merged. (It also refuses to merge if notes/.last_run says AUDIT: FAIL.)
- So "commit to main" in the steps below means: commit + push your branch with
  AUDIT: PASS recorded, and CI lands it on `main`. The next run will see it.

## WEEKLY
- Every 7th chapter, the /audit command runs instead. Do not write a chapter
  on an audit run. The audit checks the BIG picture first (plan position,
  clocks, cast, voice vs Ch1), then the small tics. See .claude/commands/audit.md.
