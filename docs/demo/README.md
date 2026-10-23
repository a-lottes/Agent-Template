# BL-AT 2026 · Live-Demo „Claude Skills richtig einsetzen“

## Start hier: [ANLEITUNG.md](ANLEITUNG.md)

Die Live-Demo in vier Schritten, alles in diesem Repo-Ordner:

1. adesso AI Hub zeigen und Provider wechseln
2. Skill bauen: Aufgaben aus Notizen und diktierten Todos
3. Skill erweitern: Ergebnisse als Markdown **und** PDF
4. Skill erweitern: Aufgaben als GitHub-Issues

Die Prompts liegen als Dateien in [prompts/](prompts/README.md) und werden mit `@` an Claude übergeben, z. B. `Führe @docs/demo/prompts/02-build.md aus.`

## Branches

| Branch | Rolle |
|---|---|
| `demo/01-ai-hub` | **Startpunkt.** Von hier aus wird `demo/live` angelegt, auf dem live gebaut wird |
| `demo/02-skill-use` | Referenz: fertiger Stand nach Schritt 2 |
| `demo/03-skill-pdf` | Referenz: fertiger Stand nach Schritt 3 |
| `demo/04-skill-github` | Referenz: fertiger Stand nach Schritt 4 |
| `demo/05-skill-check` | Referenz: zusätzlich Validierung und Eval-Fälle (optional) |
| `demo/00-setup` | Basis mit Doku und Hilfsskripten |

Alle Dokumente liegen identisch in jedem dieser Branches.

## Detail-Dokumente pro Schritt

| Schritt | Detail | Visuell |
|---|---|---|
| Überblick und Setup | [00-setup/ABLAUF.md](00-setup/ABLAUF.md) | [00-setup/VISUELL.md](00-setup/VISUELL.md) |
| 1 · AI Hub | [01-ai-hub/ABLAUF.md](01-ai-hub/ABLAUF.md) | [01-ai-hub/VISUELL.md](01-ai-hub/VISUELL.md) |
| 2 · Skill bauen | [02-skill-use/ABLAUF.md](02-skill-use/ABLAUF.md) | [02-skill-use/VISUELL.md](02-skill-use/VISUELL.md) |
| 3 · PDF | [03-skill-pdf/ABLAUF.md](03-skill-pdf/ABLAUF.md) | [03-skill-pdf/VISUELL.md](03-skill-pdf/VISUELL.md) |
| 4 · GitHub-Issues | [04-skill-github/ABLAUF.md](04-skill-github/ABLAUF.md) | [04-skill-github/VISUELL.md](04-skill-github/VISUELL.md) |
| optional · Prüfen | [05-skill-check/ABLAUF.md](05-skill-check/ABLAUF.md) | [05-skill-check/VISUELL.md](05-skill-check/VISUELL.md) |

## Archiv

Ältere Varianten mit separatem Workspace `~/agent-demo` und Branch-Wechseln liegen in [archiv/](archiv/). Sie funktionieren weiterhin, sind aber nicht mehr der empfohlene Weg.
