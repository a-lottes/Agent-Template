# 03 · Skill anpassen: Markdown **und** PDF (Detail für Jan)

Branch: `demo/03-skill-pdf` · baut auf `demo/02-skill-use` auf · Dauer live: ca. 4 Minuten · Profil: `anthropic`

## Botschaft

> „Unser Steering-Komitee liest keine Markdown-Dateien. Zwei Zeilen im Skill und ein kleines Skript, und jedes Ergebnis liegt zusätzlich als PDF daneben. Markdown bleibt die Quelle, das PDF ist das Lieferobjekt.“

## Was in diesem Branch dazukommt

| Datei | Änderung |
|---|---|
| `skills/meeting-to-actions/SKILL.md` | **neuer Schritt 6** (2 Zeilen), siehe unten. Version 0.3.0 |
| `skills/meeting-to-actions/scripts/md_to_pdf.py` | Exporter ohne Abhängigkeiten: Überschriften, Listen, Zitate, Tabellen mit Rahmen, Kopf-/Fußzeile, A4 |
| `commands/weekly-status.md` | Bericht wird zusätzlich als `status-draft.pdf` gespeichert |
| `docs/demo/backup/03-skill-pdf/` | Ergebnisse der Generalprobe (Plan B) |

Die eigentliche Skill-Änderung, das ist alles, was ihr live zeigt:

```markdown
6. Save every memory file as PDF next to its Markdown (`actions.md` + `actions.pdf`, …):
   `python3 ${CLAUDE_SKILL_DIR}/scripts/md_to_pdf.py memory`
   Markdown stays the source of truth; never edit the PDFs.
```

### Drei Lektionen, die in der Generalprobe aufgefallen sind (gut für Q&A)

1. **`${CLAUDE_SKILL_DIR}`** wird von Claude Code durch den Ordner des Skills ersetzt. Damit findet der Skill sein Skript, egal wo das Plugin installiert ist.
2. **Deterministisches gehört in ein Skript.** PDF-Layout per Prompt wäre jedes Mal anders. Das Skript macht es immer gleich, das Modell ruft es nur auf.
3. **Keine `allowed-tools`-Zeile im Skill-Frontmatter** (Stand Claude Code 2.1.274): Mit ihr wurde der Skill-Text nicht mehr geladen. Die Freigabe für das Skript steht stattdessen in `~/agent-demo/.claude/settings.json` (schreibt `setup-workspace.sh`).

Ergebnis der Generalprobe (21.10.2026, Claude): Skill-Lauf ca. 105 s, Wochenbericht ca. 25 s, ohne Rückfragen. In `memory/` liegen danach `actions`, `decisions`, `risks`, `open_questions`, `status-draft`, jeweils als `.md` und `.pdf`.

## Vorbereitung

```bash
cd ~/Documents/projects/Agent-Template
git switch demo/03-skill-pdf
demo/setup-workspace.sh
```

**Wichtig, einmalig:** `~/agent-demo` einmal **interaktiv** mit `claude` öffnen und den Vertrauensdialog („Do you trust the files in this folder?“) bestätigen. Erst danach gelten die Freigaben aus `.claude/settings.json`. Sonst fragt Claude vor dem PDF-Export nach. Das ist live auch kein Drama: einfach „Yes“ klicken.

## Live-Ablauf

### 1 · Überleitung (15 s)

*„Das Ergebnis aus Schritt 02 ist Markdown. Für das Steering-Komitee brauchen wir PDFs. Wir passen den Skill an.“*

### 2 · Die Änderung zeigen (60 s)

Im Repo, Branch `demo/03-skill-pdf`:

```bash
git diff demo/02-skill-use -- skills/meeting-to-actions/SKILL.md
```

Oder in VS Code `SKILL.md` öffnen und Schritt 6 zeigen. Kurz in `scripts/md_to_pdf.py` scrollen: *„Ein normales Python-Skript, ohne Bibliotheken. Das Layout ist fest, das Modell entscheidet nur, wann es läuft.“*

### 3 · Plugin aktualisieren, laufen lassen (2 min)

```bash
cd ~/Documents/projects/Agent-Template && demo/setup-workspace.sh
cd ~/agent-demo && claude
```

Prompt:

```
In inbox/ liegt ein neues Steering-Protokoll. Bitte aktualisiere das Projektgedächtnis.
```

Während es läuft: auf die Subagent-Aufrufe zeigen. Am Ende: `Bash(python3 …/md_to_pdf.py memory)`.

### 4 · Bericht dazu (30 s)

```
/project-memory:weekly-status
```

### 5 · Ergebnis zeigen (45 s)

```bash
open memory/status-draft.pdf memory/actions.pdf
```

*„Gleiche Inhalte, zwei Formate. Das Markdown versionieren wir, das PDF verschicken wir.“*

## Plan B

| Problem | Ausweg |
|---|---|
| Claude fragt vor dem Skript | „Yes“ wählen; Ursache: Vertrauensdialog noch nicht bestätigt |
| PDF fehlt | manuell: `python3 project-memory/skills/meeting-to-actions/scripts/md_to_pdf.py memory` |
| Lauf dauert zu lange | `open ~/Documents/projects/Agent-Template/docs/demo/backup/03-skill-pdf/*.pdf` |
| Skill-Text wirkt alt | Plugin nicht aktualisiert → `demo/setup-workspace.sh --plugin-only` |
