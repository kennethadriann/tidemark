Write the next chapter of TIDEMARK, fully following CLAUDE.md.

Steps:
1. ORIENT: read bible/canon.md, notes/state.md, notes/recap.md, and the LAST TWO
   chapter files in manuscript/ in full.
2. Determine the next chapter number NN from manuscript/_index.md.
3. GUARD: if ch(NN) already exists, or NEXT BEAT is missing/ambiguous/would reveal
   ahead of the map, STOP — write nothing, log to notes/audit.md, exit.
4. WRITE ch(NN) in the established voice, slow, ONE beat only, continuing from the
   previous chapter's exact ending. Obey the reveal map.
5. SELF-AUDIT against the CLAUDE.md checklist; rewrite once if needed.
6. SAVE manuscript/ch(NN).md.
7. RECORD: rewrite notes/state.md (advance clock, log reveals, update who/where,
   write TOMORROW'S NEXT BEAT); append 2 lines to notes/recap.md; update
   manuscript/_index.md; write "ch NN: <Title>" to notes/.last_commit_msg;
   write AUDIT: PASS/FAIL to notes/.last_run.
