---
name: meeting-to-actions
description: Use when the user provides meeting notes, transcripts, dictated todos, or project documents and wants decisions, action items, risks or open questions extracted and written to the project memory. Also applies to files in inbox/ and to German terms: Protokoll, Besprechungsnotizen, Mitschrift, Projektgedächtnis, Aufgaben, Entscheidungen, Risiken, Todos, Notizen.
---

# Meeting to actions

Project memory lives in `memory/` (decisions.md, actions.md, risks.md). Raw input lives in `inbox/`.

> **Wichtig:** "Project memory" meint immer die Dateien `memory/decisions.md`, `memory/actions.md`, `memory/risks.md` — nicht die eingebaute Claude Auto-Memory.

## Procedure

1. Delegate triage to the `project-memory:doc-triage` subagent: which inbox files are new? Run subagents in the foreground (run_in_background: false).
2. For each new file, delegate to the `project-memory:action-extractor` subagent. It returns structured findings, it does not write files. Run in the foreground (run_in_background: false).
3. Send the findings plus the source file to the `project-memory:reviewer` subagent. Apply only findings it marks `verified`. Report the rest to the user. Run in the foreground (run_in_background: false).
4. Append verified findings to `memory/decisions.md`, `memory/actions.md`, `memory/risks.md` using the tables below.
5. Append the processed file names with today's date to `memory/processed.md`.
6. Save every memory file as a PDF next to its Markdown: `python3 ${CLAUDE_SKILL_DIR}/scripts/md_to_pdf.py memory`. Markdown stays the source, never edit the PDFs by hand.
7. Summarise what was added, what was rejected and why.

## Diktierte Notizen

Wenn der Nutzer Todos oder Notizen direkt im Chat diktiert:

1. Speichere die Notiz wörtlich als `inbox/YYYY-MM-DD-<thema>.md`.
2. Eigene Todos ohne genannten Owner bekommen Owner "me".
3. Verarbeite die Inbox-Datei wie jede andere nach dem Verfahren oben.

## Schreibregel

- Schreib nur nach `memory/` und `inbox/` (für diktierte Notizen).
- Berühre nie `.env` oder Credential-Dateien.
- Frontmatter nur mit `name` und `description`, kein `allowed-tools` (damit wird der Skill korrekt geladen).

## Tabellen

### decisions.md

| Date | Decision | Decided by | Source |
|---|---|---|---|
| YYYY-MM-DD | <what was decided> | <name or TBD> | <file: quoted line> |

### actions.md

| Action | Owner | Due | Status | Source |
|---|---|---|---|---|
| <verb first> | <name or TBD> | <YYYY-MM-DD or TBD> | open | <file: quoted line> |

### risks.md

| Risk | Impact | Likelihood | Mitigation | Source |
|---|---|---|---|---|
| <risk> | low/med/high | low/med/high | <idea or TBD> | <file: quoted line> |

## Regeln

- Datum im ISO-Format `YYYY-MM-DD`.
- Herkunftsjahr aus der Notiz als Quelle angeben.
- Hedged statements ("probably", "maybe", "might", "vielleicht", "könnte", "wahrscheinlich") sind nie feste Zusagen. Als offene Frage mit Owner = `TBD` behandeln.
- Owner = `TBD`, wenn niemand genannt ist. Eigene Todos ohne genannten Owner: Owner "me".
- Nie Namen, Daten oder Zahlen erfinden. Quell-Zeile zitieren.
- Customer names und personal data aus Dateinamen halten.
