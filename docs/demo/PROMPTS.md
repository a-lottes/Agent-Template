# Spickzettel: Befehle und Prompts pro Schritt

Alles zum Kopieren, in der Reihenfolge der Demo. **Terminal** = normales Terminal (oder VS-Code-Terminal), **Claude Code** = Eingabe in der laufenden Claude-Code-Sitzung.

Repo-Pfad in den Beispielen: `~/Documents/projects/Agent-Template`. Workspace der Demo: `~/agent-demo`.

---

## Einmalig vorab (Tage vor dem Termin)

**Terminal**

```bash
cd ~/Documents/projects/Agent-Template
git fetch --all
git switch demo/01-ai-hub

scripts/provider.sh set-url https://<ai-hub-host>   # Hub-Adresse, nur lokal
scripts/provider.sh set-key                         # Hub-Key in den Schlüsselbund
scripts/model_check.py                              # Hub-Modelle testen (Tool-Calls ✓?)

gh auth status                                      # Account mit Schreibrechten aktiv?
DEMO_GH_REPO=a-lottes/Agent-Template demo/setup-workspace.sh

cd ~/agent-demo && claude                           # Vertrauensdialog bestätigen, dann /exit
```

Ein eventueller Alias `alias claude="… --settings …"` muss weg (neue Shell öffnen).

---

## Vor jedem Durchlauf (5 Minuten vorher)

**Terminal**

```bash
cd ~/Documents/projects/Agent-Template
git switch demo/01-ai-hub
DEMO_GH_REPO=a-lottes/Agent-Template demo/setup-workspace.sh
cd ~/agent-demo
claude --plugin-dir ./project-memory
```

---

## 01 · AI Hub zeigen und umschalten

`/provider` ist ein Projekt-Befehl. Er erscheint nur, wenn Claude in `~/agent-demo` (oder im Repo-Ordner) gestartet wurde. In VS Code also den Ordner `~/agent-demo` öffnen.

**Claude Code**

```
/provider
```
→ zeigt: aktuell `anthropic`.

```
/provider adesso-hub
```
→ Tabelle mit Hub-Modellen, Wechsel ist vorgemerkt.
```
/exit
```
→ Hook aktiviert den Hub.

**Terminal**

```bash
claude -c --plugin-dir ./project-memory
```

**Claude Code**

```
/status
```
→ Base URL zeigt auf den Hub.

```
Fasse inbox/2026-10-12-steering.md in drei Stichpunkten zusammen.
```

```
/provider anthropic
```
```
/exit
```

**Terminal**

```bash
claude -c --plugin-dir ./project-memory
```

**Copilot (VS Code):** Chat öffnen → Modellauswahl → „Adesso AI Hub · DeepSeek“ wählen →
```
Fasse inbox/2026-10-12-steering.md in drei Stichpunkten zusammen.
```

---

## 02 · Skill einsetzen

**Terminal** (in einem zweiten Terminal-Tab, Claude-Sitzung kann offen bleiben)

```bash
cd ~/Documents/projects/Agent-Template
git switch demo/02-skill-use
demo/setup-workspace.sh --plugin-only
claude plugin validate --strict skills
```

Claude-Sitzung neu starten, damit das Plugin neu geladen wird:

```
/exit
```
```bash
claude --plugin-dir ./project-memory
```

**Claude Code**

```
In inbox/ liegt ein neues Steering-Protokoll. Bitte aktualisiere das Projektgedächtnis.
```
→ `Skill(project-memory:meeting-to-actions)`, drei Subagents, ca. 2 Minuten.

Negativtest:

```
Was ist eine RACI-Matrix? Zwei Sätze.
```
→ Antwort **ohne** Skill.

Zeigen: `memory/actions.md` (Tabelle, Ben `2026-10-19`, Cleanup `TBD`).

---

## 03 · Skill anpassen: Markdown + PDF

**Terminal**

```bash
cd ~/Documents/projects/Agent-Template
git diff demo/02-skill-use demo/03-skill-pdf -- skills/meeting-to-actions/SKILL.md
git switch demo/03-skill-pdf
DEMO_GH_REPO=a-lottes/Agent-Template demo/setup-workspace.sh     # frisches memory/
```

```
/exit
```
```bash
cd ~/agent-demo && claude --plugin-dir ./project-memory
```

**Claude Code**

```
In inbox/ liegt ein neues Steering-Protokoll. Bitte aktualisiere das Projektgedächtnis.
```
→ am Ende `Bash(python3 …/md_to_pdf.py memory)`.

```
/project-memory:weekly-status
```

**Terminal**

```bash
open ~/agent-demo/memory/status-draft.pdf ~/agent-demo/memory/actions.pdf
```

---

## 04 · Skill anpassen: GitHub-Issues

**Terminal**

```bash
cd ~/Documents/projects/Agent-Template
git diff demo/03-skill-pdf demo/04-skill-github -- skills/meeting-to-actions/SKILL.md
git switch demo/04-skill-github
demo/setup-workspace.sh --plugin-only        # memory/ aus Schritt 03 bleibt
grep "GitHub repo" ~/agent-demo/CLAUDE.md     # muss a-lottes/Agent-Template zeigen
```

```
/exit
```
```bash
cd ~/agent-demo && claude --plugin-dir ./project-memory      # neue Sitzung, memory/ liegt auf der Platte
```

**Claude Code**

```
Lege für die offenen Aufgaben GitHub-Issues an.
```
→ Vorschau, Rückfrage.

```
Ja, bitte anlegen.
```
→ Links zu den Issues. Im Browser zeigen: `https://github.com/a-lottes/Agent-Template/issues`

Duplikat-Probe:

```
Lege für die offenen Aufgaben GitHub-Issues an.
```
→ „nichts Neues anzulegen“.

---

## 05 · Validieren und kurz evaluieren

**Terminal**

```bash
cd ~/Documents/projects/Agent-Template
git switch demo/05-skill-check
claude plugin validate --strict skills
claude plugin validate --strict commands
scripts/eval.sh anthropic --case no-trigger      # ca. 5 s
```

Nur erwähnen (Screenshot aus der Generalprobe): `scripts/skill_check.py anthropic` → 9/9.

---

## Nach der Demo

```bash
gh issue list --repo a-lottes/Agent-Template
gh issue close <nummern> --repo a-lottes/Agent-Template --comment "Live-Demo BL-AT 2026"
```

---

## Notfall: auf einen Schritt springen

```bash
cd ~/Documents/projects/Agent-Template
git switch demo/<schritt>
DEMO_GH_REPO=a-lottes/Agent-Template demo/setup-workspace.sh   # frisch
# oder: demo/setup-workspace.sh --plugin-only                   # memory/ behalten
cd ~/agent-demo && claude --plugin-dir ./project-memory
```
