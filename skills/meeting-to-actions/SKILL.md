---
name: meeting-to-actions
description: Use when the user provides meeting notes, transcripts or project documents and wants decisions, action items, risks or open questions extracted and written to the project memory.
---

# Meeting to actions

Project memory lives in `memory/` (decisions.md, actions.md, risks.md). Raw input lives in `inbox/`.

## Procedure

1. Delegate triage to the `doc-triage` subagent: which inbox files are new?
2. For each new file, delegate to the `action-extractor` subagent. It returns structured findings, it does not write files.
3. Send the findings plus the source file to the `reviewer` subagent. Apply only findings it marks `verified`. Report the rest to the user.
4. Append verified findings to `memory/decisions.md`, `memory/actions.md`, `memory/risks.md` using the templates in `templates/`.
5. Append the processed file names with today's date to `memory/processed.md`.
6. Summarise what was added, what was rejected and why.

## Rules

- Every action needs an owner and a due date. Use `TBD` when the source does not say. Never guess.
- Never invent names, dates or numbers. Quote the source line for each finding.
- Write only inside `memory/`. Never touch `.env` or credential files.
- Keep customer names and personal data out of file names.
