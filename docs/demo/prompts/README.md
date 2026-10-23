# Prompts als Dateien

Jeder Prompt aus der [Anleitung](../ANLEITUNG.md) liegt hier als eigene Datei. Du musst nichts kopieren, sondern gibst Claude Code die Datei mit `@` mit.

## So benutzt du die Dateien

In diesem Repo-Ordner (siehe [ANLEITUNG.md](../ANLEITUNG.md)):

```
Führe @docs/demo/prompts/02-build.md aus.
```

Im separaten Workspace `~/agent-demo` (ältere Variante) lautet der Pfad `@project-memory/docs/demo/prompts/…`.

Für kurze Demo-Prompts (eine Zeile) ist Tippen live oft schöner als die Datei. Beides funktioniert.

## Übersicht

| Datei | Schritt | Inhalt |
|---|---|---|
| [00-branch.md](00-branch.md) | Vorbereitung | Branch `demo/live` anlegen (alternativ per Terminal, siehe Anleitung) |
| [01-demo-summary.md](01-demo-summary.md) | 1 | Zusammenfassung auf dem AI Hub |
| [02-build.md](02-build.md) | 2 | Skill bauen (Tabellen, Hedged-Regel, diktierte Todos) und Plugin registrieren |
| [02-demo-todos.md](02-demo-todos.md) | 2 | Eigene Todos ins Projektgedächtnis |
| [03-build.md](03-build.md) | 3 | PDF-Export bauen |
| [03-demo-todos.md](03-demo-todos.md) | 3 | Weitere Todos, jetzt mit PDF |
| [04-build.md](04-build.md) | 4 | GitHub-Issues bauen |
| [04-demo-issues.md](04-demo-issues.md) | 4 | Issues anlegen (erst Vorschau) |
| [99-after-demo.md](99-after-demo.md) | danach | Offene Issues auflisten |
| [02-demo-skill.md](02-demo-skill.md) | optional | Meeting-Protokoll aus `inbox/` verarbeiten |
| [02-demo-raci.md](02-demo-raci.md) | optional | Negativtest: Skill darf nicht auslösen |
| [05-build.md](05-build.md), [05-check.md](05-check.md) | optional | Eval-Fälle bauen und prüfen |

Slash-Befehle (`/provider …`, `/actions`, `/project-memory:weekly-status`) und kurze Antworten („Ja, bitte anlegen.“) tippst du direkt.
