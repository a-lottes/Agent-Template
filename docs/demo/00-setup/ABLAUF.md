# 00 · Setup und Gesamtablauf (Detail für Jan)

Branch: `demo/00-setup` · Basis: `main` (Project-Memory-Plugin aus Teil 1)

## Ziel der Demo

Das Publikum sieht live und in einfachen Schritten:

1. **adesso AI Hub zeigen:** Claude Code (und GitHub Copilot) können statt Anthropic den Hub nutzen. Umschalten per `/provider` direkt in Claude Code. Der Rest der Demo läuft mit den Original-Claude-Modellen (schneller, zuverlässiger).
2. **Skill einsetzen:** Aufbau, wann er auslöst, was er erzeugt.
3. **Skill anpassen (1):** Ergebnisse und Berichte zusätzlich als PDF, parallel zu Markdown.
4. **Skill anpassen (2):** Offene Aufgaben später per `gh` als GitHub-Issues anlegen.
5. **Validieren und kurz evaluieren:** `claude plugin validate` plus ein kurzer Prüflauf. Nur erwähnen und zeigen, nicht vertiefen.

Roter Faden: *„Ein Skill ist eine Anleitung, die man wie Code behandelt: klein anfangen, gezielt erweitern, prüfen.“*

## Was in diesem Branch dazukommt

| Datei | Zweck |
|---|---|
| `demo/setup-workspace.sh` | Legt `~/agent-demo` an bzw. setzt es zurück (Inbox, leeres `memory/`, CLAUDE.md, Kopie des Plugins, Freigaben für die Skill-Skripte). `--plugin-only` aktualisiert nur das Plugin |
| `docs/demo/README.md` | Branch-Übersicht und Sprunganleitung |
| `.gitignore` | Ignoriert `settings.local.json` (Provider) und `evals/results/` |

## Branch-Kette

```
main ── 00-setup ── 01-ai-hub ── 02-skill-use ── 03-skill-pdf ── 04-skill-github ── 05-skill-check
```

Jeder Branch enthält alles aus den vorherigen. Korrekturen immer im frühesten betroffenen Branch machen und nach vorne mergen:

```bash
git switch demo/01-ai-hub && git merge demo/00-setup
git switch demo/02-skill-use && git merge demo/01-ai-hub
# … usw.
```

## Zeitplan (Vorschlag, ca. 20 Minuten)

| Zeit | Block | Branch | Modus |
|---|---|---|---|
| 0:00–1:00 | Einstieg: „Wohin gehen die Daten? Und wie passe ich einen Skill an?“ | – | Folie |
| 1:00–4:00 | AI Hub zeigen: Profil, `/provider`, Copilot-Dropdown | `01-ai-hub` | Live |
| 4:00–8:00 | Skill einsetzen: Aufbau, Auslösen, Ergebnis | `02-skill-use` | Live |
| 8:00–12:00 | Skill anpassen: Markdown + PDF | `03-skill-pdf` | Live |
| 12:00–16:00 | Skill anpassen: GitHub-Issues per `gh` | `04-skill-github` | Live |
| 16:00–18:30 | Validieren + kurzer Prüflauf | `05-skill-check` | Live |
| 18:30–20:00 | Fazit und Übergabe an Q&A | – | Folie |

Ab Schritt 02 läuft alles mit dem Profil `anthropic`.

## Vorbereitung (einmalig)

1. Repo klonen bzw. `git fetch --all`. Alle sechs `demo/*`-Branches liegen auf `origin`, lokal anlegen mit `git switch demo/01-ai-hub` usw.
2. `demo/setup-workspace.sh` ausführen. Ergebnis: `~/agent-demo` mit Inbox und leerem `memory/`.
3. Ab Branch 01: Hub-Adresse und Key lokal hinterlegen (`scripts/provider.sh set-url …`, `scripts/provider.sh set-key`), siehe [01-ai-hub/ABLAUF.md](../01-ai-hub/ABLAUF.md).
4. Für Schritt 04: Ziel-Repo für Issues ist dieses Repo `a-lottes/Agent-Template`, `gh` mit einem Account mit Schreibrechten (siehe [04-skill-github/ABLAUF.md](../04-skill-github/ABLAUF.md)).
5. Generalprobe: jeden Branch einmal komplett durchspielen, Laufzeiten notieren.
6. Terminal-Schrift ≥ 18 pt, VS Code Zoom ≥ 150 %, Benachrichtigungen aus, Hotspot als WLAN-Fallback.

## Vor jedem Durchlauf

```bash
cd ~/Documents/projects/Agent-Template
git switch demo/01-ai-hub          # Startpunkt der Live-Demo
demo/setup-workspace.sh
```

## Plan B (übergreifend)

| Problem | Ausweg |
|---|---|
| Ein Schritt scheitert | Nächsten Branch auschecken, `demo/setup-workspace.sh`, weiter |
| Hub nicht erreichbar | Hub-Teil überspringen, `/provider anthropic` ist ohnehin der Standard |
| Lauf dauert zu lange | Vorher aufgezeichnete Ergebnisse zeigen (Screenshots/Report aus der Generalprobe in `docs/demo/backup/` ablegen) |
| VS Code hängt | Gleiches im normalen Terminal, alles ist CLI-fähig |

## Typische Stolperfallen

- **Ein `claude`-Alias mit `--settings …`** (z. B. in `~/.zshrc`) hat höhere Priorität als jedes Projekt-Profil und hebelt `/provider` aus. Für die Demo entfernen oder `command claude` verwenden.
- **Keys nie im Klartext** in Settings-Dateien. Die Profile holen den Hub-Key per `apiKeyHelper` aus dem Schlüsselbund (`scripts/provider.sh set-key`). Settings-Dateien mit Keys nie auf dem Beamer öffnen.
- **Vertrauensdialog:** Den Workspace einmal interaktiv mit `claude` öffnen und bestätigen, sonst gelten die Freigaben aus `.claude/settings.json` nicht.
- Persönliche Notizen zur eigenen Umgebung gehören in `docs/demo/PERSOENLICH.md` (gitignored), nicht ins Repo.
