# 00 · Setup und Gesamtablauf (Detail für den Vortragenden)

Ausgangspunkt ist das Project-Memory-Plugin aus Teil 1 (`main`). Die Demo läuft komplett in **diesem Repo-Ordner**, in einer Claude-Code-Umgebung (CLI oder VS-Code-Panel). Die Schritt-für-Schritt-Anleitung steht in [ANLEITUNG.md](../ANLEITUNG.md), die Prompts in [prompts/](../prompts/README.md).

## Ziel der Demo

1. **adesso AI Hub zeigen:** Claude Code kann statt Anthropic den Hub nutzen, Umschalten per `/provider`.
2. **Skill bauen:** Aufgaben aus Notizen und diktierten Todos extrahieren.
3. **Skill erweitern:** Ergebnisse zusätzlich als PDF.
4. **Skill erweitern:** offene Aufgaben als GitHub-Issues.

Roter Faden: *„Ein Skill ist eine Anleitung, die man wie Code behandelt: klein anfangen, gezielt erweitern, prüfen.“*

## Branches

| Branch | Rolle |
|---|---|
| `demo/01-ai-hub` | **Startpunkt.** Von hier wird `demo/live` angelegt, auf dem live gebaut wird (ohne Commits) |
| `demo/02-skill-use`, `demo/03-skill-pdf`, `demo/04-skill-github` | Referenz und Backup: fertiger Stand nach dem jeweiligen Bauschritt |
| `demo/05-skill-check` | Referenz: zusätzlich Validierung und Eval-Fälle (optional) |
| `demo/00-setup` | Basis mit Doku und Hilfsskripten |

Einen fertigen Stand holst du ohne Merge mit `git restore --source demo/0X-… -- <pfade>`, siehe [ANLEITUNG.md](../ANLEITUNG.md) unter „Wenn etwas hakt“.

## Hilfsskripte

| Datei | Zweck |
|---|---|
| `demo/reset.sh` | Startzustand: Beispielprotokoll in `inbox/`, leeres `memory/`, Provider `anthropic`, keine Plugin-Registrierung |
| `scripts/provider.sh` | Provider-Profile (`anthropic`, `adesso-hub`, `adesso-hub-claude`), Hub-Adresse (`set-url`) und Key (`set-key`) |
| `.claude/commands/provider.md` | `/provider` in Claude Code |
| `.claude/commands/actions.md` | `/actions`: offene Aufgaben, Entscheidungen und Risiken aus `memory/` |

`inbox/` und `memory/` sind per `.gitignore` ausgeschlossen.

## Zeitplan (ca. 15 Minuten)

| Zeit | Block |
|---|---|
| 0:00 | Einstieg: „Wohin gehen die Daten? Und wie passe ich einen Skill an?“ |
| 0:30 | 1 · Hub-Konfiguration zeigen, `/provider` wechseln |
| 2:30 | 2 · Skill bauen (ca. 45 s), Skill zeigen, Todos eintragen, `/actions` |
| 6:00 | 3 · PDF-Export bauen (ca. 2 min), Diff zeigen, Todos + PDF |
| 10:00 | 4 · GitHub-Issues bauen (ca. 1 min), Diff zeigen, Vorschau, anlegen, Browser |
| 13:30 | Fazit |

## Vorbereitung

Siehe [ANLEITUNG.md](../ANLEITUNG.md): einmalig Hub-Adresse und Key hinterlegen, `gh auth status` prüfen, Vertrauensdialog bestätigen. Vor jedem Durchlauf den Block „Startzustand herstellen“ ausführen.

## Stolperfallen

- **Neue Session nach jedem Bauschritt**, sonst kennt Claude den geänderten Skill nicht.
- **Keine Commits:** Die Bau-Prompts lassen die Änderungen im Working Tree, damit der Diff in VS Code sichtbar ist. Nach dem Zeigen alles stagen, dann zeigt der nächste Diff nur den neuen Schritt.
- **Ein `claude`-Alias mit `--settings …`** (z. B. in `~/.zshrc`) überstimmt `/provider`. Für die Demo entfernen.
- **Keys nie im Klartext** in eingecheckten Dateien. Der Hub-Key kommt per `apiKeyHelper` aus dem Schlüsselbund (`scripts/provider.sh set-key`).
- **Hub-Modelle sind für Agenten-Läufe deutlich langsamer.** Deshalb laufen die Bauschritte mit `anthropic`.
