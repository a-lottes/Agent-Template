# Live-Demo: einen Claude-Skill bauen und erweitern

Alles läuft in **einem Ordner** (diesem Repo) und in **einer** Claude-Code-Umgebung, zum Beispiel dem VS-Code-Panel. Nach jedem Bauschritt öffnest du eine **neue Session**, damit Claude den geänderten Skill lädt.

Die Prompts liegen als Dateien in [prompts/](prompts/README.md). Du übergibst sie mit `@`:

```
Führe @docs/demo/prompts/02-build.md aus.
```

| Schritt | Was passiert | Dauer (ca.) |
|---|---|---|
| 1 | adesso-AI-Hub-Konfiguration zeigen und Provider wechseln | 2 min |
| 2 | Skill für Aufgaben bauen, eigene Todos eintragen | 3 min |
| 3 | Skill erweitern: Markdown **und** PDF | 3 min |
| 4 | Skill erweitern: Aufgaben als GitHub-Issues | 3 min |

---

## Vorbereitung (einmalig, vor der Demo)

```bash
git clone https://github.com/a-lottes/Agent-Template.git && cd Agent-Template
git switch demo/01-ai-hub
scripts/provider.sh set-url https://<ai-hub-host>   # nur für den AI-Hub-Teil
scripts/provider.sh set-key                         # Hub-Key in den Schlüsselbund
gh auth status                                      # für Schritt 4: Schreibrechte aufs Repo?
```

Danach den Ordner in VS Code öffnen, eine Claude-Session starten und den Vertrauensdialog bestätigen.

## Startzustand herstellen (vor jedem Durchlauf)

```bash
git reset --hard && git clean -fd      # verwirft die nicht committeten Änderungen eines vorigen Durchlaufs
git switch demo/01-ai-hub
git branch -D demo/live 2>/dev/null
git switch -c demo/live
demo/reset.sh
```

`git clean -fd` entfernt nur ungetrackte Dateien, keine von Git ausgeschlossenen. `providers/.hub-url`, `.claude/settings.local.json`, `inbox/` und `memory/` bleiben also erhalten.

`demo/reset.sh` legt `inbox/` mit einem Beispielprotokoll an, leert `memory/`, stellt den Provider auf `anthropic` und entfernt eine alte Plugin-Registrierung. `inbox/` und `memory/` sind von Git ausgeschlossen.

## Diff pro Schritt (ohne Commits)

Die Bau-Prompts committen nicht. Die Änderungen bleiben sichtbar in VS Code unter Source Control (`Ctrl+Shift+G`), ein Klick auf eine Datei zeigt den Diff.

Damit beim nächsten Schritt nur dessen Änderungen zu sehen sind, **stagst du nach dem Zeigen alles** (in Source Control das **+** neben „Changes“, oder `git add -A`). Dann gilt:

- **Staged Changes:** alles aus den vorigen Schritten
- **Changes:** nur der aktuelle Schritt

---

## Schritt 1 · adesso AI Hub zeigen und wechseln

**Zeigen** (im Editor öffnen):

- [`automation/ai-hub/settings.example.json`](../../automation/ai-hub/settings.example.json): So sieht eine Claude-Code-Konfiguration für den Hub aus. Base-URL, drei Modell-Aliase, Key per `apiKeyHelper`, keine Telemetrie.
- [`providers/adesso-hub.json`](../../providers/adesso-hub.json): dasselbe als umschaltbares Profil.

**Wechseln** (in Claude):

```
/provider adesso-hub
```

Neue Session öffnen, dann:

```
/status
```

```
Fasse inbox/2026-10-12-steering.md in drei Stichpunkten zusammen.
```

Auf dem Hub den kurzen Prompt lieber tippen als `@datei` übergeben. Qwen löst Dateiverweise deutlich langsamer auf.

Zurück zum Original:

```
/provider anthropic
```

Neue Session öffnen. Ab hier läuft alles mit den Anthropic-Modellen. Auf dem Hub dauern Skill-Läufe mit Subagents in Tests mehrere Minuten, mit Claude etwa eine.

In der CLI statt „neue Session“: `/exit`, dann `claude -c`.

---

## Schritt 2 · Skill für Aufgaben bauen

```
Führe @docs/demo/prompts/02-build.md aus.
```

Claude baut den Skill, prüft ihn mit `claude plugin validate` und registriert das Plugin für diesen Ordner. Committet wird nicht. **Neue Session öffnen.**

**Zeigen:** VS Code → Source Control (`Ctrl+Shift+G`): alle Änderungen des Schritts als Diff, vor allem [`skills/meeting-to-actions/SKILL.md`](../../skills/meeting-to-actions/SKILL.md). Die Beschreibung ist die Schnittstelle, die Anleitung die Implementierung, und die Tabellen stehen direkt im Skill.

**Benutzen:**

```
Führe @docs/demo/prompts/02-demo-todos.md aus.
```

Claude speichert die Todos als Notiz in `inbox/` und schickt sie durch Triage, Extraktion und Review. Das Ergebnis landet in `memory/actions.md`. „Vielleicht …“ wird dabei keine feste Aufgabe.

```
/actions
```

zeigt alle offenen Aufgaben als Tabelle.

---

## Schritt 3 · Skill erweitern: Markdown + PDF

```
Führe @docs/demo/prompts/03-build.md aus.
```

**Neue Session öffnen.**

**Zeigen:** Source Control in VS Code. Unter „Changes“ steht nur, was dieser Schritt geändert hat (siehe „Diff pro Schritt“ oben).

Neu ist Schritt 6, ein Aufruf von `scripts/md_to_pdf.py`. Das Layout steckt im Skript, das Modell entscheidet nur, wann es läuft.

**Benutzen:**

```
Führe @docs/demo/prompts/03-demo-todos.md aus.
```

```bash
open memory/actions.pdf
```

Optional den Wochenbericht als PDF erzeugen: `/project-memory:weekly-status`, dann `open memory/status-draft.pdf`.

---

## Schritt 4 · Skill erweitern: Aufgaben als GitHub-Issues

```
Führe @docs/demo/prompts/04-build.md aus.
```

**Neue Session öffnen.**

**Zeigen:** Source Control in VS Code, darin den neuen Abschnitt im Skill, „Later: action items as GitHub issues“. Issues entstehen nur auf Wunsch, nach einer Vorschau und ohne Duplikate.

**Benutzen:**

```
Führe @docs/demo/prompts/04-demo-issues.md aus.
```

Claude zeigt eine Vorschau und fragt nach. Dann:

```
Ja, bitte anlegen.
```

Die Issues landen im GitHub-Repo dieses Checkouts. Zum Abschluss im Browser die Issue-Liste zeigen. In `memory/actions.md` steht jetzt `open · #<nummer>`.

---

## Danach

```
Führe @docs/demo/prompts/99-after-demo.md aus.
```

Danach die Demo-Issues nach Bestätigung schließen. Die Plugin-Registrierung entfernt `demo/reset.sh` beim nächsten Durchlauf.

## Wenn etwas hakt

| Problem | Ausweg |
|---|---|
| Ein Bau-Prompt liefert Murks oder dauert zu lang | Fertigen Stand aus dem Referenz-Branch holen, ohne Merge und ohne Stagen: `git restore --source demo/02-skill-use -- skills agents .claude-plugin README.md` (bzw. `demo/03-skill-pdf`, `demo/04-skill-github` mit `skills commands .claude-plugin`). Die Dateien erscheinen unter „Changes“. Nach Schritt 2 das Plugin registrieren (nächste Zeile) |
| Skill wird nach dem Bauen nicht verwendet | Neue Session geöffnet? Nach Schritt 2 muss das Plugin registriert sein: `claude plugin marketplace add . --scope local` und `claude plugin install project-memory@adesso-agent-demo --scope local` |
| `/provider adesso-hub` meldet einen `apiKeyHelper`-Fehler | Key fehlt: `scripts/provider.sh set-key` |
| Claude fragt nach Freigaben | Zustimmen, das ist beim Bauen normal |

## Validieren und evaluieren (zum Nachlesen)

Prüf- und Eval-Skripte gibt es im Referenz-Branch `demo/05-skill-check`: `claude plugin validate --strict`, `scripts/eval.sh` (Eval-Fälle mit `claude plugin eval`) und `scripts/skill_check.py`. Details stehen in [05-skill-check/ABLAUF.md](05-skill-check/ABLAUF.md).
