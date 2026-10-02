Write the next chapter of TIDEMARK, fully following CLAUDE.md.

Steps:
1. ORIENT: read bible/canon.md (incl. the STORY PLAN), notes/state.md,
   notes/recap.md, manuscript/ch01.md + manuscript/ch06.md (VOICE ANCHOR),
   and the LAST TWO chapter files in manuscript/ in full (continuity).
2. Determine the next chapter number NN from manuscript/_index.md.
3. GUARD: if ch(NN) already exists, or NEXT BEAT is missing/ambiguous/would reveal
   ahead of the map, STOP — write nothing, log to notes/audit.md, exit.
4. PLAN CHECK: find NN's milestone in the STORY PLAN. If NN is at/past a
   milestone's "no later than" chapter, this chapter's beat IS that milestone.
5. WRITE ch(NN) in the Ch1/Ch6 voice. ONE beat that CHANGES something,
   continuing from the previous chapter's ending (time skips allowed).
6. SELF-AUDIT against the CLAUDE.md checklist; rewrite once if needed.
7. SAVE manuscript/ch(NN).md.
8. RECORD: rewrite notes/state.md (≤ ~4 KB, keep its headings, update CLOCK and
   PLAN POSITION, write TOMORROW'S NEXT BEAT); append 2 lines to notes/recap.md;
   update manuscript/_index.md; write "ch NN: <Title>" to notes/.last_commit_msg;
   write AUDIT: PASS/FAIL to notes/.last_run.
