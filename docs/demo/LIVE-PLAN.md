# Live-Plan: alles live bauen auf `demo/live` (ohne Branch-Wechsel und Merges)

Ab jetzt wird alles live auf **einem** Branch `demo/live` gebaut. Die Branches `demo/00-setup` … `demo/05-skill-check` sind nur noch **Backup und Referenz**. Jeder Bauschritt endet mit einem Commit, so zeigt `git log` den Fortschritt.

Zwei Claude-Code-Sitzungen laufen nebeneinander:

| Sitzung | Ordner | Wofür |
|---|---|---|
| **Repo-Session** | `~/Documents/projects/Agent-Template` | Bau-Prompts: Claude ändert Skill, Skripte, Commands und committet |
| **Demo-Session** | `~/agent-demo` | Demo-Prompts: der Agent arbeitet mit dem gerade gebauten Plugin |

Beide Sitzungen laufen mit dem Provider `anthropic`. Nur in Schritt 01 wird der Hub gezeigt.

Abgleich mit dem Referenzstand, ohne zu mergen: `git diff demo/02-skill-use -- skills/` (analog für die anderen Schritte).

---

## Was beim Prüfen des Plans aufgefallen ist (bereits in die Prompts unten eingearbeitet)

Diese Punkte haben in den Generalproben Fehler verursacht. Weil Claude den Code live selbst schreibt, stehen sie jetzt explizit in den Bau-Prompts:

1. **Kein `allowed-tools` im Frontmatter** von `SKILL.md` und den Commands. Mit dieser Zeile wurde der Skill nicht mehr geladen (Claude Code 2.1.274). Freigaben für Skripte stehen stattdessen in `~/agent-demo/.claude/settings.json`, die schreibt `setup-workspace.sh`.
2. **`/project-memory:create-issues`** muss den Skill ausdrücklich als `project-memory:meeting-to-actions` über das Skill-Tool aufrufen. Sonst sucht Claude den Skill im Dateisystem.
3. **Der Dry-Run-Test in `/tmp`** braucht `--repo a-lottes/Agent-Template`, weil es dort keine `CLAUDE.md` gibt.
4. **Schritt 05:** Auf `demo/live` gibt es noch keine Eval-Dateien als Vorlage. Die Vorlage liegt im Referenz-Branch (`git show demo/05-skill-check:evals/…`). Dazu kommen die bekannten Stolperfallen von `claude plugin eval`:
   - `execution.env` in `case.yaml` erlaubt nur `EVAL_*`-Variablen.
   - Regex-Flags gehören in `flags: i`, nicht als `(?i)` in das Muster.
   - Plugin-Subagents erkennt man per `regex` auf `trace`, nicht per `tool_used: Agent`.
   - Skill-Läufe brauchen `timeout_seconds: 600` und in `allowed_tools` auch `Task, Agent, Skill`.
5. **`skill_check.py`** braucht in `claude -p` eine Freigabe für `md_to_pdf.py` (`--settings` mit einer Allow-Regel) und `--add-dir <repo>`. Sonst bleibt der PDF-Export an einer Rückfrage hängen.
6. **Reihenfolge:** Schritt 0 muss **vor** `setup-workspace.sh` laufen. Das Skript kopiert das Plugin aus dem Branch, der gerade ausgecheckt ist.
7. **Zeitbedarf:** Ein Bau-Prompt braucht live ca. 2–5 Minuten. Für Schritt 03 und 05, bei denen viel Code entsteht, die Wartezeit mit Erklärungen füllen oder den Referenz-Diff zeigen.

---

## Vorab (vor dem Termin, einmalig)

Siehe [PROMPTS.md](PROMPTS.md), Abschnitt „Einmalig vorab“: Hub-Adresse und Key hinterlegen, `gh auth status` prüfen, den Vertrauensdialog in `~/agent-demo` **und** im Repo-Ordner bestätigen.

---

## Schritt 0 · Arbeitsbranch anlegen (Repo-Session)

```
Lege einen Branch demo/live an, ausgehend vom aktuellen Stand demo/01-ai-hub, und wechsle darauf. Keine Dateiänderungen. Zeig danach git status und git log --oneline -3.
```

Falls `demo/live` aus einer Generalprobe noch existiert, vorher im Terminal löschen: `git switch demo/01-ai-hub && git branch -D demo/live`.

---

## Schritt 01 · AI Hub zeigen (nichts zu bauen, Demo-Session)

**Terminal** (nach Schritt 0, vor dem Termin):

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
Fasse inbox/2026-10-12-steering.md in drei Stichpunkten zusammen.
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

## Schritt 02 · Skill einsetzen (Bau-Prompt, Repo-Session)

```
Baue Schritt 02 auf dem Branch demo/live. Kein Merge, nur Dateien bearbeiten. Ziel:

1. Neu: .claude-plugin/marketplace.json mit name "adesso-agent-demo", owner.name "adesso BL-AT 2026", metadata.description "Demo marketplace for the BL-AT 2026 hands-on: Claude skills with the adesso AI Hub.", und plugins[0] = { name "project-memory", source "./", description "Turns meeting notes into decisions, actions and risks, with review and guardrails." }.
2. .claude-plugin/plugin.json: version 0.1.0 → 0.2.0.
3. README.md, Abschnitt "Package for a team" ersetzen: Das Repo ist zugleich Marketplace. Befehle: /plugin marketplace add <Repo-Pfad oder Git-URL> und /plugin install project-memory@adesso-agent-demo.
4. agents/action-extractor.md und agents/reviewer.md: Hedged-Regel ergänzen. Hedged Aussagen ("probably", "maybe", "might") sind nie feste Zusagen, Owner = TBD plus offene Frage. Datumsformat ISO YYYY-MM-DD.
5. skills/meeting-to-actions/SKILL.md überarbeiten:
   - Description: auch für Dateien in inbox/, und für deutsche Begriffe (Protokoll, Besprechungsnotizen, Mitschrift, Projektgedächtnis, Aufgaben, Entscheidungen, Risiken).
   - Im Kopf: "Project memory" meint immer memory/decisions.md, actions.md, risks.md, nicht die eingebaute Auto-Memory.
   - Subagents immer im Vordergrund ausführen (run_in_background: false) und mit Prefix aufrufen: project-memory:doc-triage, project-memory:action-extractor, project-memory:reviewer.
   - Schritt 4: Die Tabellen direkt im SKILL.md angeben, nicht über templates/:
     decisions.md: | Date | Decision | Decided by | Source | mit Zeile | YYYY-MM-DD | <what was decided> | <name or TBD> | <file: quoted line> |
     actions.md: | Action | Owner | Due | Status | Source | mit Zeile | <verb first> | <name or TBD> | <YYYY-MM-DD or TBD> | open | <file: quoted line> |
     risks.md: | Risk | Impact | Likelihood | Mitigation | Source | mit Zeile | <risk> | low/med/high | low/med/high | <idea or TBD> | <file: quoted line> |
   - Regeln ergänzen: Datum ISO, Herkunftsjahr aus der Notiz, hedged statements als offene Frage.
   - Wichtig: kein allowed-tools im Frontmatter (damit wird der Skill nicht geladen). Frontmatter nur name und description.
6. Lösche skills/meeting-to-actions/templates/ (actions.md, decisions.md, risks.md).

Danach: claude plugin validate --strict skills und claude plugin validate --strict agents ausführen und Ergebnis zeigen. Zum Schluss committen: "Demo 02: Skill einsetzen (Marketplace, Tabellen im Skill, Hedged-Regel)".
```

**Terminal** (Repo-Ordner; das Plugin wird kopiert und registriert, `memory/` bleibt):

```bash
demo/setup-workspace.sh --plugin-only
```

Dann in `~/agent-demo`: `/exit` und `claude`.

**Demo-Session:**

```
In inbox/ liegt ein neues Steering-Protokoll. Bitte aktualisiere das Projektgedächtnis.
```
```
Was ist eine RACI-Matrix? Zwei Sätze.
```

Erwartet: `Skill(project-memory:meeting-to-actions)` und drei Subagents. Die RACI-Frage wird ohne Skill beantwortet.

---

## Schritt 03 · Skill anpassen: Markdown + PDF (Bau-Prompt, Repo-Session)

```
Baue Schritt 03 auf demo/live, ohne Merge. Ziel:

1. Neu: skills/meeting-to-actions/scripts/md_to_pdf.py (ausführbar, Python-Standardbibliothek, keine Abhängigkeiten).
   - Aufruf: md_to_pdf.py memory (alle *.md im Ordner, außer processed.md) oder md_to_pdf.py memory/actions.md (einzelne Datei). Ohne Argument: Hilfetext ausgeben.
   - Schreibt die PDF neben die .md (actions.md → actions.pdf) und gibt "<md> -> <pdf>" aus.
   - A4 Hochformat, Helvetica (Standard-Font, WinAnsi-Encoding), Kopfzeile "Project Memory · <Titel>" mit Datum, Seitenzahl "n / m" unten.
   - Unterstützt: Überschriften, Absätze, Aufzählungen (•), Zitate (grau, eingerückt), Pipe-Tabellen mit Kopfzeile in Fettschrift und Spaltenbreiten passend zum Text, Zeilenumbruch in Zellen. Inline-Markdown (**fett**, `code`, Links) als Klartext.
   - PDF von Hand schreiben (Objekte, xref, Trailer), ohne Bibliotheken.
   - Ein Dokumentationskopf mit den Aufrufbeispielen.
2. skills/meeting-to-actions/SKILL.md: Schritt 6 neu: Jede Memory-Datei als PDF neben das Markdown speichern, Aufruf python3 ${CLAUDE_SKILL_DIR}/scripts/md_to_pdf.py memory. Markdown bleibt die Quelle, PDFs nie von Hand bearbeiten. Danach ist Schritt 7 die Zusammenfassung. Kein allowed-tools im Frontmatter.
3. commands/weekly-status.md: description um "(Markdown and PDF)" ergänzen. Am Ende den Befehl python3 ${CLAUDE_PLUGIN_ROOT}/skills/meeting-to-actions/scripts/md_to_pdf.py memory/status-draft.md anhängen, mit dem Satz, dass die PDF neben dem Markdown gespeichert wird. Kein allowed-tools im Frontmatter.
4. .claude-plugin/plugin.json: version 0.2.0 → 0.3.0.

Test: Mit den Beispieldateien aus examples/ ein Test-Memory in /tmp bauen (kein Eingriff ins Repo) und md_to_pdf.py darauf laufen lassen. Dann file <pdf> prüfen und mir Ausgabe zeigen. Committen: "Demo 03: Markdown + PDF-Export".
```

**Terminal** (frisches `memory/`):

```bash
DEMO_GH_REPO=a-lottes/Agent-Template demo/setup-workspace.sh
```

Dann in `~/agent-demo`: `/exit` und `claude`.

**Demo-Session:**

```
In inbox/ liegt ein neues Steering-Protokoll. Bitte aktualisiere das Projektgedächtnis.
```
```
/project-memory:weekly-status
```

→ Terminal: `open ~/agent-demo/memory/status-draft.pdf ~/agent-demo/memory/actions.pdf`

---

## Schritt 04 · Skill anpassen: GitHub-Issues (Bau-Prompt, Repo-Session)

```
Baue Schritt 04 auf demo/live, ohne Merge. Ziel:

1. Neu: skills/meeting-to-actions/scripts/create_issues.py (ausführbar, Standardbibliothek plus gh CLI).
   - Aufruf: create_issues.py memory/actions.md --dry-run (nur Vorschau) und create_issues.py memory/actions.md (anlegen). Optional --repo owner/name.
   - Zielrepo: --repo, sonst Env-Variable PROJECT_MEMORY_GH_REPO, sonst die Zeile "GitHub repo for action items: owner/name" in ./CLAUDE.md. Sonst mit Fehlermeldung abbrechen.
   - Liest die Tabelle mit Kopfzeile | Action | Owner | Due | Status | Source | über die Spaltennamen, nicht über feste Positionen.
   - Nur Zeilen mit Status "open" ohne "#<zahl>" bearbeiten, damit Wiederholungen keine Duplikate erzeugen.
   - Titel = Action, Body = Owner, Due, Source plus Hinweis "Created by the project-memory agent".
   - Ohne --dry-run: gh issue create ausführen, Status auf "open · #<nummer>" setzen und die Datei zurückschreiben. Bei gh-Fehler mit Meldung abbrechen.
2. Neu: commands/create-issues.md mit description "Turn open action items from memory/actions.md into GitHub issues (preview first, then create)." Der Befehl ruft den Skill project-memory:meeting-to-actions ausdrücklich über das Skill-Tool auf (nicht im Dateisystem suchen) und folgt dessen Abschnitt für Issues. Die Vorschau muss vor dem Anlegen bestätigt werden. Kein allowed-tools im Frontmatter.
3. skills/meeting-to-actions/SKILL.md:
   - Description um "Also when open action items should become GitHub issues" und deutsche Begriffe (Issues/Tickets anlegen) erweitern.
   - Neuer Abschnitt "Later: action items as GitHub issues", nur auf ausdrückliche Bitte. Schritt 1: Vorschau mit python3 ${CLAUDE_SKILL_DIR}/scripts/create_issues.py memory/actions.md --dry-run und Bestätigung durch den Nutzer. Schritt 2: nach Bestätigung ohne --dry-run. Schritt 3: PDFs neu rendern und Issue-Links melden.
4. .claude-plugin/plugin.json: version 0.3.0 → 0.4.0.

Test: Den Dry-Run gegen eine Test-actions.md in /tmp laufen lassen, mit --repo a-lottes/Agent-Template (dort gibt es keine CLAUDE.md). Kein echtes Anlegen. Committen: "Demo 04: Action items als GitHub-Issues".
```

**Terminal** (Repo-Ordner, `memory/` bleibt):

```bash
demo/setup-workspace.sh --plugin-only
grep "GitHub repo" ~/agent-demo/CLAUDE.md
```

Der `grep` muss `a-lottes/Agent-Template` zeigen. Dann in `~/agent-demo`: `/exit` und `claude`. Bewusst eine **neue** Sitzung, nicht `-c`: Im fortgesetzten Gespräch hat Claude in der Generalprobe die geänderten Projektdateien misstrauisch hinterfragt.

**Demo-Session:**

```
Lege für die offenen Aufgaben GitHub-Issues an.
```
```
Ja, bitte anlegen.
```

Duplikat-Probe:

```
Lege für die offenen Aufgaben GitHub-Issues an.
```

→ Erwartet: „nichts Neues anzulegen“.

---

## Schritt 05 · Validieren und kurz evaluieren (Bau-Prompt, Repo-Session)

```
Baue Schritt 05 auf demo/live, ohne Merge. Als Vorlage für Format und Stil dienen die Dateien im Referenz-Branch, nur lesen, nicht mergen: git show demo/05-skill-check:evals/steering-notes/case.yaml, git show demo/05-skill-check:evals/no-trigger/case.yaml, git show demo/05-skill-check:scripts/eval.sh. Ziel:

1. Eval-Fälle unter evals/:
   - evals/scaffold-inbox.sh: Shared Scaffold. Aufruf: scaffold-inbox.sh <inbox|later>/<datei> [--with-claude-md]. Legt inbox/ und memory/ an, kopiert eine Beispieldatei aus examples/ und optional examples/CLAUDE.md.
   - evals/steering-notes/scaffold.sh: ruft scaffold-inbox.sh mit inbox/2026-10-12-steering.md --with-claude-md auf (ausführbar).
   - evals/steering-notes/case.yaml: Happy Path. Prompt "Process the new meeting notes in inbox/ into the project memory." Graders: Skill meeting-to-actions wurde aufgerufen; Trace enthält subagent_type project-memory:reviewer; memory/actions.md und decisions.md haben die exakten Tabellen-Kopfzeilen; "Ben … 2026-10-19" steht drin; Cleanup-Owner ist TBD; ein LLM-Grader prüft, dass nichts erfunden ist (Ben, Clara, offene DPIA-Freigabe).
   - evals/no-trigger/case.yaml: Prompt "What is a RACI matrix? Answer in two sentences.", Skill darf nicht feuern, memory/actions.md darf nicht existieren, Antwort enthält responsib|accountab.
   Schema: schema_version 1.0, runs 1, graders mit type tool_used / regex / file_exists / llm.
   Stolperfallen beachten: execution.env erlaubt nur EVAL_*-Variablen; Regex-Flags als "flags: i", nicht "(?i)"; den Reviewer-Subagent per regex auf target trace prüfen (nicht tool_used Agent); bei Skill-Läufen timeout_seconds 600 und allowed_tools [Read, Glob, Grep, Write, Edit, Task, Agent, Skill]; "Skill darf nicht feuern" als tool_used mit min 0, max 0, arm both.
2. scripts/eval.sh (ausführbar): Argumente <profile> [--case …] [--runs n], Standard-Profil anthropic. Lädt die Provider-Umgebung über scripts/provider.sh env <profile>, setzt CLAUDE_CODE_DISABLE_AUTO_MEMORY=1, validiert Plugin, Skills und Agents mit claude plugin validate --strict, startet dann claude plugin eval . --scaffold --trust-plugin --allow-tools Write Edit --ablation none --runs 1 -j 4 --no-publish plus Restargumente.
3. scripts/skill_check.py (ausführbar, Standardbibliothek): führt die Fälle schnell mit claude -p in frischen Temp-Workspaces parallel aus (Befehlszeile mit --plugin-dir <repo>, --add-dir <repo>, --permission-mode acceptEdits, --setting-sources project,local, --settings mit einer Allow-Regel "Bash(python3 <repo>/skills/meeting-to-actions/scripts/md_to_pdf.py *)", --output-format stream-json --verbose, Env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1), wertet Tool-Aufrufe und memory/*.md per Regex aus und gibt einen Score aus (z. B. 9/9). Fälle: steering-notes (inkl. actions.pdf vorhanden), vague-owner (Erik 2026-10-24, Load test nicht an Ben), no-trigger. Profil als erstes Argument, Standard anthropic.
4. Prüfen: claude plugin validate --strict commands, dann scripts/eval.sh anthropic --case no-trigger, Ausgabe zeigen.

Committen: "Demo 05: Validierung und Eval-Fälle".
```

**Repo-Session, danach zur Kontrolle:**

```
Führe aus: claude plugin validate --strict skills, claude plugin validate --strict commands und scripts/eval.sh anthropic --case no-trigger. Zeig mir die Ausgaben.
```

Optional (ca. 2,5 Minuten, nur erwähnen oder Screenshot): `scripts/skill_check.py anthropic`.

---

## Nach der Demo (Repo-Session)

```
Liste die offenen Issues in a-lottes/Agent-Template auf. Schließe noch nichts, ich sage dir welche.
```

Danach die Demo-Issues nach Bestätigung mit dem Kommentar „Live-Demo BL-AT 2026“ schließen. Achtung: Die Issues #1–#3 aus der Generalprobe sind ebenfalls noch offen.

Aufräumen der Plugin-Registrierung: `claude plugin marketplace remove adesso-agent-demo`.

---

## Notfall

| Problem | Ausweg |
|---|---|
| Ein Bau-Prompt liefert Murks | Abgleich ohne Merge: `git diff demo/0X-… -- <pfad>`. Notfalls die Datei aus dem Referenz-Branch holen: `git checkout demo/0X-… -- <pfad>`, dann committen |
| Ein Bau-Prompt dauert zu lang | Gleiches wie oben: Dateien aus dem Referenz-Branch holen, Diff zeigen und erklären |
| Live geht gar nichts mehr | Auf den fertigen Referenz-Branch springen, wie in [PROMPTS.md](PROMPTS.md) unter „Notfall“ beschrieben |
| Skill lädt nicht (`Execute skill` ohne Inhalt) | `allowed-tools` im Frontmatter? Zeile entfernen, `demo/setup-workspace.sh --plugin-only`, neue Sitzung |

## Hinweise

- Die Bau-Prompts sind Spezifikationen. Claude schreibt den Code selbst, deshalb können Wortlaut und Details vom Referenz-Branch abweichen. Das ist für die Demo unkritisch, solange `validate` und die Demo-Prompts funktionieren.
- Der **Code** in `backup/*` und `demo/0X-*` bleibt unverändert. In den `demo/0X-*`-Branches kommt nur diese Datei dazu. Die Notfall-Befehle aus [PROMPTS.md](PROMPTS.md) funktionieren weiterhin.
- `demo/live` muss nicht gepusht werden. Wer das Repo klont, startet mit Schritt 0 selbst.
