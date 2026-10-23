# Live-Plan: alles live bauen auf `demo/live` (ohne Branch-Wechsel und Merges)

> **Archiv:** Ältere Variante mit separatem Workspace `~/agent-demo` und Branch-Wechseln. Sie funktioniert weiterhin, ist aber nicht mehr der empfohlene Weg. **Aktuell gilt [ANLEITUNG.md](../ANLEITUNG.md).**

> Für einen 15-Minuten-Slot gibt es die gekürzte Fassung [LIVE-15MIN.md](LIVE-15MIN.md).

Ab jetzt wird alles live auf **einem** Branch `demo/live` gebaut. Die Branches `demo/00-setup` … `demo/05-skill-check` sind nur noch **Backup und Referenz**. Jeder Bauschritt endet mit einem Commit, so zeigt `git log` den Fortschritt.

Zwei Claude-Code-Sitzungen laufen nebeneinander:

| Sitzung | Ordner | Wofür |
|---|---|---|
| **Repo-Session** | `~/Documents/projects/Agent-Template` | Bau-Prompts: Claude ändert Skill, Skripte, Commands und committet |
| **Demo-Session** | `~/agent-demo` | Demo-Prompts: der Agent arbeitet mit dem gerade gebauten Plugin |

Beide Sitzungen laufen mit dem Provider `anthropic`. Nur in Schritt 01 wird der Hub gezeigt.

**Alle Prompts liegen als einzelne Dateien in [prompts/](../prompts/README.md).** Du gibst sie Claude mit `@` mit, statt sie zu kopieren:

| Sitzung | So rufst du einen Prompt auf |
|---|---|
| Repo-Session | `Führe @docs/demo/prompts/02-build.md aus.` |
| Demo-Session | `Führe @project-memory/docs/demo/prompts/02-demo-skill.md aus.` |

Abgleich mit dem Referenzstand, ohne zu mergen: `git diff demo/02-skill-use -- skills/` (analog für die anderen Schritte).

---

## Vorab (vor dem Termin, einmalig)

Siehe [PROMPTS.md](PROMPTS.md), Abschnitt „Einmalig vorab“: Hub-Adresse und Key hinterlegen, `gh auth status` prüfen, den Vertrauensdialog in `~/agent-demo` **und** im Repo-Ordner bestätigen.

Falls `demo/live` aus einer Generalprobe noch existiert, vorher löschen:

```bash
cd ~/Documents/projects/Agent-Template
git switch demo/01-ai-hub && git branch -D demo/live
```

---

## Schritt 0 · Arbeitsbranch anlegen (Repo-Session)

```
Führe @docs/demo/prompts/00-branch.md aus.
```

---

## Schritt 01 · AI Hub zeigen (nichts zu bauen, Demo-Session)

**Terminal** (nach Schritt 0, denn das Skript kopiert das Plugin aus dem ausgecheckten Branch):

```bash
cd ~/Documents/projects/Agent-Template
DEMO_GH_REPO=a-lottes/Agent-Template demo/setup-workspace.sh
cd ~/agent-demo && claude
```

**Claude Code:**

```
/provider
```
```
/provider adesso-hub
```
```
/exit
```
→ Terminal: `claude -c` (VS Code: neue Konversation im Claude-Panel)
```
/status
```
```
Führe @project-memory/docs/demo/prompts/01-demo-summary.md aus.
```
```
/provider anthropic
```
```
/exit
```
→ Terminal: `claude -c`

In diesem Schritt ist das Plugin noch nicht geladen. Es wird erst ab Schritt 02 registriert, weil erst dann ein Marketplace existiert.

---

## Schritt 02 · Skill einsetzen

**Repo-Session:**

```
Führe @docs/demo/prompts/02-build.md aus.
```

**Terminal** (Repo-Ordner; das Plugin wird kopiert und registriert, `memory/` bleibt):

```bash
demo/setup-workspace.sh --plugin-only
```

Dann in `~/agent-demo`: `/exit` und `claude`.

**Demo-Session:**

```
Führe @project-memory/docs/demo/prompts/02-demo-skill.md aus.
```
```
Führe @project-memory/docs/demo/prompts/02-demo-raci.md aus.
```

Erwartet: `Skill(project-memory:meeting-to-actions)` und drei Subagents. Die RACI-Frage wird ohne Skill beantwortet.

---

## Schritt 03 · Skill anpassen: Markdown + PDF

**Repo-Session:**

```
Führe @docs/demo/prompts/03-build.md aus.
```

**Terminal** (frisches `memory/`):

```bash
DEMO_GH_REPO=a-lottes/Agent-Template demo/setup-workspace.sh
```

Dann in `~/agent-demo`: `/exit` und `claude`.

**Demo-Session:**

```
Führe @project-memory/docs/demo/prompts/02-demo-skill.md aus.
```
```
/project-memory:weekly-status
```

→ Terminal: `open ~/agent-demo/memory/status-draft.pdf ~/agent-demo/memory/actions.pdf`

---

## Schritt 04 · Skill anpassen: GitHub-Issues

**Repo-Session:**

```
Führe @docs/demo/prompts/04-build.md aus.
```

**Terminal** (Repo-Ordner, `memory/` bleibt):

```bash
demo/setup-workspace.sh --plugin-only
grep "GitHub repo" ~/agent-demo/CLAUDE.md
```

Der `grep` muss `a-lottes/Agent-Template` zeigen. Dann in `~/agent-demo`: `/exit` und `claude`. Bewusst eine **neue** Sitzung, nicht `-c`: Im fortgesetzten Gespräch hat Claude in der Generalprobe die geänderten Projektdateien misstrauisch hinterfragt.

**Demo-Session:**

```
Führe @project-memory/docs/demo/prompts/04-demo-issues.md aus.
```
```
Ja, bitte anlegen.
```

Duplikat-Probe:

```
Führe @project-memory/docs/demo/prompts/04-demo-issues.md aus.
```

→ Erwartet: „nichts Neues anzulegen“.

---

## Schritt 05 · Validieren und kurz evaluieren

**Repo-Session:**

```
Führe @docs/demo/prompts/05-build.md aus.
```

Danach zur Kontrolle:

```
Führe @docs/demo/prompts/05-check.md aus.
```

Optional (ca. 2,5 Minuten, nur erwähnen oder Screenshot): `scripts/skill_check.py anthropic`.

Warum der Eval über `adesso-hub` läuft: Die Eval-Sandbox von `claude plugin eval` übernimmt den `env`-Block aus der globalen `~/.claude/settings.json`. Zeigt die (wie bei Jan) auf den Hub, kommen dort nur Hub-Modelle an. Mit `adesso-hub` und Qwen läuft der Kurz-Eval in ca. 3 Sekunden, souverän und kostenlos. Auf einem Rechner ohne globale Hub-Konfiguration geht auch `scripts/eval.sh anthropic --case no-trigger`.

---

## Nach der Demo (Repo-Session)

```
Führe @docs/demo/prompts/99-after-demo.md aus.
```

Danach die Demo-Issues nach Bestätigung mit dem Kommentar „Live-Demo BL-AT 2026“ schließen. Achtung: Die Issues #1–#3 aus der Generalprobe sind ebenfalls noch offen.

Aufräumen der Plugin-Registrierung: `claude plugin marketplace remove adesso-agent-demo`.

---

## Was in den Prompts steckt (Erkenntnisse aus den Generalproben)

Weil Claude den Code live selbst schreibt, stehen bekannte Stolperfallen ausdrücklich in den Bau-Prompts:

1. **Kein `allowed-tools`** im Frontmatter von `SKILL.md` und den Commands. Mit dieser Zeile wurde der Skill nicht geladen. Die Freigaben für Skripte stehen in `~/agent-demo/.claude/settings.json`, die schreibt `setup-workspace.sh`.
2. **`/project-memory:create-issues`** ruft den Skill ausdrücklich über das Skill-Tool auf, sonst sucht Claude ihn im Dateisystem.
3. **Tests in `.scratch/` im Repo** (per `.gitignore` ausgeschlossen) statt in `/tmp`. Schreiben nach `/tmp` liegt außerhalb des Projekts und braucht eine Freigabe. In der Generalprobe blieb der Bauschritt daran hängen und wurde nicht committet.
4. **Dry-Run mit `--repo a-lottes/Agent-Template`**, weil es in `.scratch/` keine `CLAUDE.md` gibt.
5. **Schritt 05** liest die Vorlagen per `git show demo/05-skill-check:…` und kennt die Eval-Stolperfallen: `execution.env` nur `EVAL_*`, Regex-Flags als `flags: i`, Subagent-Prüfung per `trace`, Timeout 600 s, Modell aus dem Profil an `--model` und `--judge-model` durchreichen.
6. **`skill_check.py`** bekommt eine Allow-Regel für `md_to_pdf.py` und `--add-dir`, sonst hängt der PDF-Export an einer Rückfrage.
7. **Jeder Bauschritt prüft am Ende `git status`**, damit nichts uncommittet liegen bleibt.

8. **Freigaben auch für `python3 -I …`**: Claude ruft Skripte manchmal im isolierten Modus auf. `setup-workspace.sh` erlaubt beide Varianten.

**Zeitbedarf** laut zweiter Generalprobe (22.10.2026, mit den Prompt-Dateien): Schritt 0 ca. 10 s, Schritt 02 ca. 40 s, Schritt 03 ca. 2 min, Schritt 04 ca. 50 s, Schritt 05 ca. 50 s. Ein Demo-Skill-Lauf dauert ca. 60–75 s, der Kurz-Eval ca. 3 s.

**Im Bau fragt Claude interaktiv gelegentlich nach Freigaben** (zusammengesetzte Shell-Befehle). Einfach zustimmen, das ist im Repo normal.

---

## Notfall

| Problem | Ausweg |
|---|---|
| Ein Bau-Prompt liefert Murks | Abgleich ohne Merge: `git diff demo/0X-… -- <pfad>`. Notfalls die Datei aus dem Referenz-Branch holen: `git checkout demo/0X-… -- <pfad>`, dann committen |
| Ein Bau-Prompt dauert zu lang | Wie oben: Dateien aus dem Referenz-Branch holen, Diff zeigen und erklären |
| Bauschritt fragt nach Freigaben | Zustimmen. Im Repo sind Schreib- und Git-Befehle normal |
| Live geht gar nichts mehr | Auf den fertigen Referenz-Branch springen, siehe [PROMPTS.md](PROMPTS.md) unter „Notfall“ |
| Skill lädt nicht (`Execute skill` ohne Inhalt) | `allowed-tools` im Frontmatter? Zeile entfernen, `demo/setup-workspace.sh --plugin-only`, neue Sitzung |
| Eval meldet 403 `not available for this API key` | Mit `scripts/eval.sh adesso-hub --case no-trigger` starten (siehe Schritt 05) |

## Hinweise

- Die Bau-Prompts sind Spezifikationen. Claude schreibt den Code selbst, deshalb können Wortlaut und Details vom Referenz-Branch abweichen. Das ist für die Demo unkritisch, solange `validate` und die Demo-Prompts funktionieren.
- Der Code in `backup/*` und `demo/0X-*` bleibt unverändert. Ausnahmen: In allen Branches kommen nur die Doku, `.scratch/` in der `.gitignore` und die Modell-Weitergabe in `scripts/eval.sh` (Referenz 05) dazu.
- `demo/live` muss nicht gepusht werden. Wer das Repo klont, startet mit Schritt 0 selbst.
