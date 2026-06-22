# TIDEMARK — writing instructions (read this every run)

You are writing a serialized sci-fi/dystopian novel, one chapter per run.
The repo is the memory. You start cold every run; reconstruct state from files.

## VOICE (non-negotiable)
- First person, past tense, narrator = Adz.
- Plain English. Bob Ong style: short sentences, dry humor, conversational,
  grounded, easy for people who don't read much.
- NO Taglish in the prose. (Filipino names and food are fine and good.)
- NO "AI cadence." Specifically avoid:
  - the "Short. Punchy. Dramatic." staccato one-line-paragraph pile-up
  - rule-of-three triplets ("smart, precise, and allergic to...")
  - a profound "button" line at the end of every paragraph
  - em-dash overuse
  - every sentence reaching for meaning. Let plain things stay plain.
- A couple of dry jokes per chapter. Warmth. Real human texture.

## PACING (non-negotiable)
- SLOW BURN. One chapter = ONE beat. Do not advance plot to feel productive.
- Most chapters should NOT end on a cliffhanger. Quiet endings are good.
- Chapter length: ~900–1300 words.

## BEFORE WRITING — orient (always, in this order)
1. Read bible/canon.md — the secret truth + the REVEAL MAP. Never state canon
   outright. Never reveal anything ahead of its scheduled arc.
2. Read notes/state.md — the clock, who/where, revealed-so-far, and NEXT BEAT.
3. Read notes/recap.md — the running synopsis.
4. Read the LAST TWO chapter files in manuscript/ IN FULL — match the voice to
   this real prose, not to this description. This is the main anti-drift anchor.

## GUARD — before you write
- If manuscript/ already has a file for today's chapter number: STOP, write nothing.
- If NEXT BEAT is missing, ambiguous, or would force a reveal ahead of the map:
  WRITE NOTHING. Append a note to notes/audit.md explaining why, and exit.
  A skipped day is fine. A wrong chapter on main is not.

## WRITE
- Continue from the previous chapter's exact final moment.
- Execute ONLY the NEXT BEAT. Obey the reveal map.
- Title the chapter "## Chapter NN — <Title>". End with "*End of Chapter NN.*".

## SELF-AUDIT — before saving, re-read your own draft against this checklist
- [ ] Voice matches the last 2 chapters (plain, dry, not AI-cadence)?
- [ ] No staccato pile-ups, no triplets, no per-paragraph profundity?
- [ ] Exactly ONE beat advanced? Slow?
- [ ] Nothing revealed ahead of the map?
- [ ] No Taglish in prose?
If ANY box fails: rewrite ONCE. If it still fails, write "AUDIT: FAIL" to
notes/.last_run (otherwise write "AUDIT: PASS") and still save the draft — the
git wrapper will quarantine it on its branch instead of merging to main.

## AFTER WRITING — record (this is what makes tomorrow flow)
1. Save manuscript/chNN.md.
2. REWRITE notes/state.md: advance the clock, log what you revealed, update
   who/where, and WRITE TOMORROW'S NEXT BEAT (replace the NEXT BEAT section).
3. Append ~2 lines to notes/recap.md for this chapter.
4. Update manuscript/_index.md (mark NN done, add NN+1 pending).
5. Write the commit message to notes/.last_commit_msg as:  ch NN: <Title>
6. Write "AUDIT: PASS" or "AUDIT: FAIL" to notes/.last_run.

## WEEKLY
- Every 7th chapter, the /audit command runs instead: read the last 7 chapters
  + recap and write an honest voice/pace drift check to notes/audit.md. Do not
  write a chapter on an audit run.
