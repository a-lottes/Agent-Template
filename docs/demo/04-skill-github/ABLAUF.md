# 04 · Skill anpassen: Aufgaben als GitHub-Issues (Detail für Jan)

Branch: `demo/04-skill-github` · baut auf `demo/03-skill-pdf` auf · Dauer live: ca. 4 Minuten · Profil: `anthropic`

## Botschaft

> „Aufgaben, die nur in einer Datei stehen, werden vergessen. Mit einem kleinen Zusatz im Skill wandern offene Aufgaben auf Wunsch als Issues nach GitHub, mit Vorschau und erst nach Bestätigung. Der Mensch bleibt in der Schleife.“

## Was in diesem Branch dazukommt

| Datei | Änderung |
|---|---|
| `skills/meeting-to-actions/SKILL.md` | **neuer Abschnitt „Later: action items as GitHub issues“** + Auslöser in der Beschreibung. Version 0.4.0 |
| `skills/meeting-to-actions/scripts/create_issues.py` | liest `memory/actions.md`, legt per `gh issue create` Issues an, schreibt `#<nr>` in die Status-Spalte |
| `commands/create-issues.md` | expliziter Befehl `/project-memory:create-issues` |
| `examples/CLAUDE.md` | Zeile `GitHub repo for action items: <owner/repo>` (steht schon ab Schritt 00 drin, damit sie live nicht „neu“ auftaucht) |
| `demo/setup-workspace.sh` | setzt das Ziel-Repo aus `DEMO_GH_REPO` in die Workspace-CLAUDE.md und merkt es sich |

Die Skill-Änderung, die ihr live zeigt:

```markdown
## Later: action items as GitHub issues

Only when the user asks for it (e.g. "create issues for the open actions", "Tickets anlegen"):

1. Preview: `python3 ${CLAUDE_SKILL_DIR}/scripts/create_issues.py memory/actions.md --dry-run`.
   Show the list and ask the user to confirm.
2. After the user confirms: run the same command without `--dry-run`. It writes `#<issue>`
   into the Status column, so re-runs never create duplicates.
3. Re-render the PDFs (step 6) and report the issue links.
```

### Designentscheidungen (für Q&A)

- **„Später“ statt automatisch:** Issues entstehen nur auf Wunsch. Ein Skill-Lauf erzeugt keine Seiteneffekte nach außen, ohne dass jemand zustimmt.
- **Vorschau zuerst (`--dry-run`):** Claude zeigt die Liste und wartet auf „ja“.
- **Idempotent:** Die Issue-Nummer steht danach in `actions.md` (`open · #12`). Ein zweiter Lauf legt nichts doppelt an.
- **`gh` statt eigener API-Anbindung:** nutzt eure bestehende GitHub-Anmeldung, kein Token in Dateien.
- **Owner bleibt Text im Issue-Body:** Vornamen sind keine GitHub-Logins. Eine Zuordnung Name → Login wäre der nächste Ausbauschritt.

Generalprobe (21.10.2026, Claude, Ziel-Repo `a-lottes/Agent-Template`):

1. „Lege für die offenen Aufgaben GitHub-Issues an.“ → Skill löst aus, Vorschau mit 3 Issues, Rückfrage
2. „Ja, bitte anlegen.“ → Issues [#1](https://github.com/a-lottes/Agent-Template/issues/1), [#2](https://github.com/a-lottes/Agent-Template/issues/2), [#3](https://github.com/a-lottes/Agent-Template/issues/3) angelegt, `actions.md` zeigt `open · #1` usw., PDFs neu erzeugt
3. Gleiche Bitte erneut → „nichts Neues anzulegen“ (keine Duplikate)

## Vorbereitung

1. **Ziel-Repo ist dieses Repo:** `a-lottes/Agent-Template` (öffentlich, Issues aktiv). Der aktive `gh`-Account braucht Schreibrechte auf das Repo. Prüfen mit `gh auth status`, bei mehreren Accounts mit `gh auth switch` den richtigen aktiv setzen.
2. Workspace mit Ziel-Repo aufsetzen:
   ```bash
   cd ~/Documents/projects/Agent-Template
   git switch demo/04-skill-github
   DEMO_GH_REPO=a-lottes/Agent-Template demo/setup-workspace.sh
   ```
3. **Vor dem Termin die Test-Issues aus der Generalprobe schließen** (#1–#3), damit live nur die neuen zu sehen sind:
   ```bash
   gh issue close 1 2 3 --repo a-lottes/Agent-Template --comment "Demo-Generalprobe"
   ```
   Achtung: Das Repo ist öffentlich, die Demo-Daten sind fiktiv, trotzdem keine echten Projektdaten verwenden.
4. Den Browser-Tab `https://github.com/a-lottes/Agent-Template/issues` vorab öffnen.

## Live-Ablauf

### 1 · Überleitung (15 s)

*„Die Aufgaben stehen jetzt als Markdown und PDF da. Damit sie bearbeitet werden, gehören sie ins Ticketsystem.“*

### 2 · Die Änderung zeigen (60 s)

```bash
git diff demo/03-skill-pdf -- skills/meeting-to-actions/SKILL.md
```

Drei Dinge betonen: *nur auf Wunsch*, *erst Vorschau*, *keine Duplikate*.

### 3 · Plugin aktualisieren, ohne `memory/` zu verlieren (10 s)

```bash
cd ~/Documents/projects/Agent-Template && DEMO_GH_REPO=a-lottes/Agent-Template demo/setup-workspace.sh --plugin-only
```

Hinweis: `--plugin-only` behält `memory/` aus Schritt 03. Das Ziel-Repo merkt sich der Workspace (`.claude/gh-repo`), sobald es einmal mit `DEMO_GH_REPO=…` gesetzt wurde. Die Zeile `GitHub repo for action items` steht ab Schritt 00 in der `CLAUDE.md`.

### 4 · Issues anlegen (90 s)

In einer **neuen** Claude-Code-Sitzung (`/exit`, dann `claude`). Die Ergebnisse aus Schritt 03 liegen ja in `memory/`. Hintergrund: Setzt man das alte Gespräch mit `-c` fort, kann Claude geänderte Projektdateien misstrauisch hinterfragen. Das ist gutes Verhalten, kostet live aber Zeit:

```
Lege für die offenen Aufgaben GitHub-Issues an.
```

oder explizit `/project-memory:create-issues`.

- Claude zeigt die Vorschau (3 Issues) und fragt nach → *„Der Agent fragt, bevor er nach außen handelt.“*
- `ja` tippen → Issues entstehen, Links werden ausgegeben.

### 5 · Ergebnis zeigen (45 s)

- Browser (`github.com/a-lottes/Agent-Template/issues`): neue Issues, Body mit Owner, Fälligkeit und Quellzitat.
- `memory/actions.md`: Status jetzt `open · #1` usw.
- Gleiche Bitte noch einmal: *„Nothing to do“*. → *„Keine Duplikate.“*

## Plan B

| Problem | Ausweg |
|---|---|
| `No target repo` | Zeile `GitHub repo for action items: owner/repo` in `~/agent-demo/CLAUDE.md` ergänzen |
| `gh` nicht angemeldet / falscher Account | `gh auth status`, `gh auth switch` |
| Claude fragt vor dem Skript | „Yes“ wählen (Vertrauensdialog noch nicht bestätigt) |
| Netz weg | Nur den Probelauf zeigen: `python3 project-memory/skills/meeting-to-actions/scripts/create_issues.py memory/actions.md --dry-run` |
