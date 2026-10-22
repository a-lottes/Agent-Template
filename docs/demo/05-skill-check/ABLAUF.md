# 05 · Validieren und kurz evaluieren (Detail für Jan)

Branch: `demo/05-skill-check` · baut auf `demo/04-skill-github` auf · Dauer live: ca. 2 Minuten · Profil: `anthropic`

## Botschaft

> „Wir haben den Skill zweimal geändert. Woher wissen wir, dass er noch tut, was er soll? Validieren prüft die Form, ein kurzer Eval-Lauf prüft das Verhalten. Das gehört zu jeder Änderung, wie Tests zu Code.“

Nur **erwähnen und kurz zeigen**, nicht vertiefen.

## Was in diesem Branch dazukommt

| Datei | Zweck |
|---|---|
| `evals/steering-notes/`, `evals/no-trigger/` | zwei Testfälle im offiziellen Format von `claude plugin eval` (`case.yaml`) |
| `scripts/eval.sh [profil] [optionen]` | `claude plugin validate --strict` + `claude plugin eval` mit Provider-Profil |
| `scripts/skill_check.py [profil] [fälle]` | einfacher Check: führt den Skill wie ein Nutzer aus (parallel) und prüft die Ergebnisdateien |

Was geprüft wird:

| Fall | Prüfungen |
|---|---|
| `steering-notes` | Skill löst aus · Plugin-Reviewer genutzt · Tabellenformat · ISO-Datum · **PDF neben Markdown** |
| `vague-owner` (nur `skill_check.py`) | „Probably Ben …“ wird keine feste Zuweisung · ISO-Datum |
| `no-trigger` | allgemeine Frage → Skill bleibt aus, Frage beantwortet |

Generalprobe 21.10.2026, Profil `anthropic`:

| Lauf | Dauer | Ergebnis |
|---|---|---|
| `claude plugin validate --strict …` | < 1 s | ✔ |
| `scripts/eval.sh adesso-hub --case no-trigger` | ca. 4 s | Score 1.00 |
| `scripts/skill_check.py anthropic no-trigger` | ca. 7 s | 2/2 |
| `scripts/skill_check.py anthropic` (alle 3 Fälle) | ca. 2,5 min | **9/9** |

## Vorbereitung

```bash
cd ~/Documents/projects/Agent-Template
git switch demo/05-skill-check
scripts/skill_check.py anthropic        # einmal komplett, Screenshot für die Folie sichern
```

## Live-Ablauf

### 1 · Validieren (20 s)

```bash
cd ~/Documents/projects/Agent-Template
claude plugin validate --strict skills
claude plugin validate --strict commands
```

*„Wie ein Linter: Struktur und Frontmatter stimmen.“*

### 2 · Ein Testfall in 20 Sekunden (40 s)

`evals/no-trigger/case.yaml` zeigen:

- `prompt`: eine Frage, die mit dem Skill nichts zu tun hat
- Grader `skill-not-fired` (`tool_used`, `max: 0`): *„Ein guter Skill springt nicht an, wenn er nicht gemeint ist.“*

### 3 · Kurzer Lauf (20 s)

```bash
scripts/eval.sh adesso-hub --case no-trigger
```

Ausgabe: Tabelle mit `no-trigger 1.00 100%`. *„Das ist das offizielle Werkzeug von Claude Code. Im Team läuft das in CI, bei jeder Skill-Änderung.“*

### 4 · Erwähnen (30 s)

Screenshot der Generalprobe zeigen (`skill_check.py anthropic`, 9/9):

*„Der volle Lauf dauert gut zwei Minuten und prüft auch, dass das PDF entsteht und vage Zusagen nicht als feste Aufgabe landen. Mit `adesso-hub` statt `anthropic` vergleicht ihr in einem Befehl, wie gut ein Hub-Modell euren Skill ausführt.“*

## Hintergrund (für Q&A)

- **`claude plugin eval`** kann mehr: KI-Richter (`type: llm`), Vergleich mit/ohne Plugin (Ablation), HTML-Report, mehrere Läufe pro Fall (`--runs 3`), Schwellwert für CI (`--threshold 0.8`).
- **Erfahrung aus der Generalprobe:** Längere Fälle mit Subagents hingen in der Eval-Sandbox teils bis zum Timeout. Deshalb live nur `no-trigger` mit `eval.sh` und für den vollen Lauf `skill_check.py`.
- **Modellvergleich** (Generalprobe 20.10., ältere Fall-Auswahl): Claude 12/12, DeepSeek über den Hub 9/12. Die Abweichungen lagen am Modell, nicht am Skill. Details im Branch `archive/03-skill-eval-detail`.

## Plan B

| Problem | Ausweg |
|---|---|
| `eval.sh` hängt oder meldet Fehler | `scripts/skill_check.py anthropic no-trigger` (gleicher Fall, ohne Sandbox) |
| Gar keine Zeit mehr | nur `claude plugin validate --strict skills` und Screenshot zeigen |
