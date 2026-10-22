# BL-AT 2026 · Live-Demo „Claude Skills richtig einsetzen“

Hands-on-Demo in sechs Schritten. Jeder Schritt ist ein eigener Branch und baut auf dem vorherigen auf.
Geht live etwas schief, springt ihr einfach auf den nächsten Branch.

| Branch | Thema | Doku (Detail) | Doku (Visuell) |
|---|---|---|---|
| `demo/00-setup` | Ausgangslage, Demo-Workspace, Gesamtablauf | [ABLAUF](00-setup/ABLAUF.md) | [VISUELL](00-setup/VISUELL.md) |
| `demo/01-ai-hub` | adesso AI Hub zeigen, `/provider` zum Umschalten, Copilot | [ABLAUF](01-ai-hub/ABLAUF.md) | [VISUELL](01-ai-hub/VISUELL.md) |
| `demo/02-skill-use` | Skill korrekt einsetzen: Aufbau, Auslösen, Ergebnis | [ABLAUF](02-skill-use/ABLAUF.md) | [VISUELL](02-skill-use/VISUELL.md) |
| `demo/03-skill-pdf` | Skill anpassen: Ergebnisse als Markdown **und** PDF | [ABLAUF](03-skill-pdf/ABLAUF.md) | [VISUELL](03-skill-pdf/VISUELL.md) |
| `demo/04-skill-github` | Skill anpassen: Aufgaben als GitHub-Issues per `gh` | [ABLAUF](04-skill-github/ABLAUF.md) | [VISUELL](04-skill-github/VISUELL.md) |
| `demo/05-skill-check` | Validieren und kurz evaluieren | [ABLAUF](05-skill-check/ABLAUF.md) | [VISUELL](05-skill-check/VISUELL.md) |

**Live-Plan (empfohlen): alles live auf einem Branch `demo/live` bauen, ohne Branch-Wechsel und Merges:** [LIVE-PLAN.md](LIVE-PLAN.md). Die `demo/0X-*`-Branches dienen dabei als Backup und Referenz. Alle Prompts liegen als einzelne Dateien in [prompts/](prompts/README.md) und lassen sich mit `@` direkt an Claude übergeben.

**Spickzettel für den Ablauf mit Branch-Wechsel (Backup-Variante):** [PROMPTS.md](PROMPTS.md)

Alle Dokumente liegen in **jedem** `demo/*`-Branch und auf `main`. Ihr könnt also von überall aus lesen, egal welcher Schritt gerade ausgecheckt ist.

## Springen, wenn live etwas hakt

```bash
cd ~/Documents/projects/Agent-Template
git switch demo/03-skill-pdf         # Ziel-Branch
demo/setup-workspace.sh              # Workspace frisch machen (Provider bleibt erhalten)
```

`demo/setup-workspace.sh` kopiert das Plugin des aktuellen Branches nach `~/agent-demo/project-memory`. Nach jedem Branch-Wechsel also einmal ausführen. Mit `--plugin-only` bleibt `memory/` erhalten (praktisch, wenn ihr mitten in der Demo auf den nächsten Schritt springt).
