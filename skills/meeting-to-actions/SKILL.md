---
name: meeting-to-actions
description: Use whenever files in inbox/ (meeting notes, minutes, transcripts, project documents) should be processed into the project memory, i.e. decisions, action items, risks or open questions written to memory/decisions.md, memory/actions.md, memory/risks.md. Also when the user dictates own todos or notes in the chat. Also for German requests (Protokoll, Besprechungsnotizen, Mitschrift, Projektgedächtnis, Aufgaben, Todos, Entscheidungen, Risiken).
---

# Meeting to actions

Project memory lives in `memory/` (decisions.md, actions.md, risks.md). Raw input lives in `inbox/`.
"Project memory" always means these files, not any built-in memory feature.

## Procedure

Run each subagent in the foreground (`run_in_background: false`) and wait for its result before the next step.

1. Delegate triage to the `project-memory:doc-triage` subagent: which inbox files are new?
2. For each new file, delegate to the `project-memory:action-extractor` subagent. It returns structured findings, it does not write files.
3. Send the findings plus the source file to the `project-memory:reviewer` subagent. Apply only findings it marks `verified`. Report the rest to the user.
4. Append verified findings to the three memory files. If a file does not exist, create it with its header row. Use exactly these tables:

   `memory/decisions.md`
   ```
   | Date | Decision | Decided by | Source |
   |---|---|---|---|
   | YYYY-MM-DD | <what was decided> | <name or TBD> | <file: quoted line> |
   ```

   `memory/actions.md`
   ```
   | Action | Owner | Due | Status | Source |
   |---|---|---|---|---|
   | <verb first> | <name or TBD> | <YYYY-MM-DD or TBD> | open | <file: quoted line> |
   ```

   `memory/risks.md`
   ```
   | Risk | Impact | Likelihood | Mitigation | Source |
   |---|---|---|---|---|
   | <risk> | low/med/high | low/med/high | <idea or TBD> | <file: quoted line> |
   ```

5. Append the processed file names with today's date to `memory/processed.md`.
6. Save every memory file as PDF next to its Markdown (`actions.md` + `actions.pdf`, …):
   `python3 ${CLAUDE_SKILL_DIR}/scripts/md_to_pdf.py memory`
   Markdown stays the source of truth; never edit the PDFs.
7. Summarise what was added, what was rejected and why, and list open questions.

## Rules

- Every action needs an owner and a due date. Use `TBD` when the source does not say. Never guess.
- Dates are ISO `YYYY-MM-DD`. Take the year from the note's own date.
- Hedged statements ("probably", "maybe", "might", "wahrscheinlich") are not assignments: owner `TBD`, and list the quoted line as an open question.
- Never invent names, dates or numbers. Quote the source line for each finding.
- Write only inside `memory/` (and `inbox/` for dictated notes). Never touch `.env` or credential files.
- Keep customer names and personal data out of file names.
- Notes or todos dictated directly in the chat: first save them verbatim as `inbox/YYYY-MM-DD-<topic>.md`, then process that file like any other inbox file. For the user's own todos without a named owner, the owner is `me`.
