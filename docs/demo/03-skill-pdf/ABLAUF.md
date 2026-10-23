# 03 · Skill erweitern: Markdown + PDF (Detail)

Teil von [ANLEITUNG.md](../ANLEITUNG.md), Schritt 3. Bau-Prompt: [prompts/03-build.md](../prompts/03-build.md). Referenzstand: Branch `demo/03-skill-pdf`.

## Botschaft

> „Das Steering-Komitee liest kein Markdown. Zwei Zeilen im Skill und ein kleines Skript, und jedes Ergebnis liegt zusätzlich als PDF daneben.“

## Was der Bau-Prompt ändert

| Datei | Änderung |
|---|---|
| `skills/meeting-to-actions/scripts/md_to_pdf.py` | neu: PDF-Export ohne Abhängigkeiten (A4, Tabellen, Kopf- und Fußzeile) |
| `skills/meeting-to-actions/SKILL.md` | neuer Schritt 6: `python3 ${CLAUDE_SKILL_DIR}/scripts/md_to_pdf.py memory` |
| `commands/weekly-status.md` | Wochenbericht zusätzlich als PDF |
| `.claude-plugin/plugin.json` | Version 0.3.0 |

Getestet wird in `.scratch/` im Repo (gitignored), nicht in `/tmp`. Schreiben nach `/tmp` braucht eine Freigabe, und in Tests blieb der Bau daran hängen.

## Was zu zeigen ist

`git diff HEAD~1 -- skills/meeting-to-actions/SKILL.md` zeigt die neue Zeile. Dazu ein kurzer Blick in `md_to_pdf.py`: *„Das Layout steckt im Skript, das Modell entscheidet nur, wann es läuft.“*

## Benutzen

- [prompts/03-demo-todos.md](../prompts/03-demo-todos.md): zwei weitere Todos. Danach liegen `memory/*.md` und `memory/*.pdf` nebeneinander.
- `open memory/actions.pdf`
- Optional `/project-memory:weekly-status`, dann `open memory/status-draft.pdf`.

## Für Fragen

- `${CLAUDE_SKILL_DIR}` ist der Ordner des Skills. So findet der Skill sein Skript, egal wo das Plugin installiert ist.
- Markdown bleibt die Quelle. PDFs werden nie von Hand bearbeitet.
