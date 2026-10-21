# 02 · Skill korrekt einsetzen (Detail für Jan)

Branch: `demo/02-skill-use` · baut auf `demo/01-ai-hub` auf · Dauer live: ca. 4 Minuten

## Botschaft

> „Ein Skill ist eine Anleitung mit einer Schnittstelle. Die Beschreibung entscheidet, *ob* er geladen wird, der Inhalt, *wie* gearbeitet wird. Wer das trennt, bekommt Skills, die zuverlässig auslösen und wenig Kontext kosten.“

## Was in diesem Branch dazukommt

| Datei | Zweck |
|---|---|
| `.claude-plugin/marketplace.json` | Macht das Repo zum Team-Marktplatz: `/plugin marketplace add` + `/plugin install` |
| `skills/meeting-to-actions/SKILL.md` | **Korrekt aufgesetzt** (Version 0.2.0), siehe unten |
| `agents/action-extractor.md`, `agents/reviewer.md` | Regeln für ISO-Datum und vage Aussagen |

Was gegenüber Teil 1 am Skill korrigiert ist (in der Generalprobe gemessen, alle Punkte führten sonst zu Fehlern):

| Problem in Teil-1-Version | Korrektur |
|---|---|
| `templates/` liegt außerhalb des Arbeitsordners, headless nicht lesbar → Format weicht ab | Tabellenformate **direkt in SKILL.md** |
| Subagents als `doc-triage` referenziert, registriert ist `project-memory:doc-triage` | voll qualifizierte Namen |
| Subagents liefen im Hintergrund, Hauptsession hing | „Run each subagent in the foreground“ |
| „project memory“ kollidiert mit Claudes eingebautem Memory | Klarstellung im Skill |
| Datum „19 Oct“ statt ISO | Regel: `YYYY-MM-DD` |
| „Probably Ben will …“ wurde feste Zuweisung | Regel: vage → `TBD` + offene Frage |

## Anatomie eines Skills (zum Zeigen)

```
skills/meeting-to-actions/
└── SKILL.md            ← Frontmatter (immer im Kontext) + Anleitung (nur bei Bedarf)
```

| Teil | Wann im Kontext? | Wofür |
|---|---|---|
| `name` + `description` | **immer** (wenige Tokens) | Claude entscheidet daran, ob der Skill passt |
| Rest von `SKILL.md` | erst wenn der Skill auslöst | Vorgehen, Regeln, Ausgabeformat |
| Skripte im Skill-Ordner | erst wenn die Anleitung sie aufruft | deterministische Schritte (kommt in Schritt 03) |

## Regeln für den korrekten Einsatz (Checkliste)

1. **Eine Aufgabe pro Skill.** „Meeting → Aktionen“, nicht „Projektmanagement allgemein“.
2. **Die Beschreibung sagt, *wann*.** Mit Auslösern, die Nutzer wirklich tippen („meeting notes“, „transcript“, ggf. deutsch).
3. **Anleitung als nummerierte Schritte**, Regeln als harte Verbote („Never invent names“).
4. **Format festlegen** (Templates), sonst variiert jede Ausgabe.
5. **Deterministisches in Skripte**, nicht in Prosa.
6. **Abhängigkeiten eindeutig benennen** (Subagents als `project-memory:reviewer`, Dateien). Was nicht eindeutig ist, findet ein schwächeres Modell nicht.
7. **Ablageort nach Reichweite:** `~/.claude/skills/` (nur ich) · `.claude/skills/` (Projekt) · Plugin (Team, versioniert).
8. **Validieren, bevor man verteilt:** `claude plugin validate --strict .`

## Vorbereitung

```bash
cd ~/Documents/projects/Agent-Template
git switch demo/02-skill-use
demo/setup-workspace.sh
# Provider: anthropic ist Standard. Prüfen in Claude Code mit /provider
```

## Live-Ablauf

### 1 · Anatomie zeigen (60 s)

`skills/meeting-to-actions/SKILL.md` öffnen.

- Frontmatter markieren: *„Das ist die Schnittstelle. Nur diese zwei Zeilen kennt Claude dauerhaft.“*
- Prozedur: *„Das ist die Implementierung. Wird erst geladen, wenn die Beschreibung passt.“*
- Tabellen am Ende von Schritt 4: *„Das Format steht direkt im Skill, damit jede Ausgabe gleich aussieht.“*

### 2 · Validieren (20 s)

```bash
cd ~/Documents/projects/Agent-Template
claude plugin validate --strict .
claude plugin validate --strict skills
```

Sagen: *„Wie ein Linter: Struktur und Frontmatter stimmen.“* (Ausführlicher in Schritt 05.)

### 3 · Automatisch auslösen lassen (90 s)

```bash
cd ~/agent-demo
claude --plugin-dir ./project-memory
```

Prompt (natürliche Sprache, kein Slash-Command):

```
In inbox/ liegt ein neues Steering-Protokoll. Bitte aktualisiere das Projektgedächtnis.
```

Zeigen:

- In der Ausgabe erscheint `Skill(project-memory:meeting-to-actions)` → *„Claude hat anhand der Beschreibung entschieden.“*
- Danach die Subagent-Aufrufe (Triage, Extraktion, Review).
- `memory/actions.md`: Ben, Schnittstellenspezifikation, Quelle zitiert. Cleanup mit Owner `TBD`.

Erwartete Laufzeit mit Claude: ca. 2 Minuten. Währenddessen Punkt 4 erklären.

### 4 · Explizit vs. automatisch (30 s, während der Lauf läuft)

| Weg | Beispiel | Wann sinnvoll |
|---|---|---|
| automatisch | natürliche Bitte | Alltag, Nutzer kennt den Skill nicht |
| explizit | `/project-memory:meeting-to-actions` oder `/project-memory:process-inbox` | Automatisierung, Headless, Reproduzierbarkeit |

### 5 · Negativtest (20 s)

```
Was ist eine RACI-Matrix? Zwei Sätze.
```

Erwartung: Antwort **ohne** Skill-Aufruf. *„Ein guter Skill löst auch *nicht* aus, wenn er nicht gemeint ist.“*

### 6 · Verteilen ans Team (30 s, nur zeigen)

```
/plugin marketplace add ~/Documents/projects/Agent-Template
/plugin install project-memory@adesso-agent-demo
```

Sagen: *„Für Kolleg:innen ist das ein Git-Repo. Installieren, fertig, gleiche Version für alle.“*
(Live nicht ausführen, sonst ist das Plugin doppelt geladen.)

## Was ihr beobachten solltet (Generalprobe 20.10.2026, Profil anthropic)

- `Skill(project-memory:meeting-to-actions)`, danach `project-memory:doc-triage`, `…:action-extractor`, `…:reviewer`
- `memory/actions.md` als Tabelle `| Action | Owner | Due | Status | Source |`, Ben mit `2026-10-19`, Cleanup mit `TBD`
- Laufzeit ca. 2–2,5 Minuten
- Überleitung: *„Das Ergebnis ist Markdown. Unser Steering-Komitee will aber PDFs. Passen wir den Skill an.“*

## Plan B

| Problem | Ausweg |
|---|---|
| Skill löst nicht automatisch aus | explizit `/project-memory:process-inbox` |
| Lauf dauert > 3 min | Ergebnis aus der Generalprobe zeigen oder auf `demo/03-skill-pdf` springen |
| Hook blockt Schreiben | Gut so, erklären: „Skill sagt *wie*, Hook sagt *was nie*“ |
