# Prompts als Dateien

Jeder Prompt aus dem [Live-Plan](../LIVE-PLAN.md) liegt hier als eigene Datei. Du musst nichts kopieren, sondern gibst Claude Code die Datei mit `@` mit.

## So benutzt du die Dateien

**Repo-Session** (Claude läuft in `~/Documents/projects/Agent-Template`):

```
Führe @docs/demo/prompts/02-build.md aus.
```

**Demo-Session** (Claude läuft in `~/agent-demo`, das Plugin liegt dort als Kopie unter `project-memory/`):

```
Führe @project-memory/docs/demo/prompts/02-demo-skill.md aus.
```

Für kurze Demo-Prompts (eine Zeile) ist Tippen live oft schöner als die Datei. Beides funktioniert.

## Übersicht

| Datei | Sitzung | Schritt | Inhalt |
|---|---|---|---|
| [00-branch.md](00-branch.md) | Repo | 0 | Branch `demo/live` anlegen |
| [01-demo-summary.md](01-demo-summary.md) | Demo | 01 | Zusammenfassung auf dem AI Hub |
| [02-build.md](02-build.md) | Repo | 02 | Skill korrekt aufsetzen (Marketplace, Tabellen, Hedged-Regel) |
| [02-demo-skill.md](02-demo-skill.md) | Demo | 02, 03 | Skill auslösen: Projektgedächtnis aktualisieren |
| [02-demo-raci.md](02-demo-raci.md) | Demo | 02 | Negativtest: Skill darf nicht auslösen |
| [03-build.md](03-build.md) | Repo | 03 | PDF-Export bauen |
| [04-build.md](04-build.md) | Repo | 04 | GitHub-Issues bauen |
| [04-demo-issues.md](04-demo-issues.md) | Demo | 04 | Issues anlegen (erst Vorschau) |
| [05-build.md](05-build.md) | Repo | 05 | Eval-Fälle und Prüfskripte bauen |
| [05-check.md](05-check.md) | Repo | 05 | Validieren und kurzer Eval-Lauf |
| [99-after-demo.md](99-after-demo.md) | Repo | danach | Offene Issues auflisten |

Slash-Befehle (`/provider …`, `/project-memory:weekly-status`) und Ein-Wort-Antworten („Ja, bitte anlegen.“) tippst du direkt, siehe [LIVE-PLAN.md](../LIVE-PLAN.md).
