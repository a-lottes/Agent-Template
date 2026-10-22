# Live-Demo in 15 Minuten (Kurzfassung des Live-Plans)

Gleicher Aufbau wie [LIVE-PLAN.md](LIVE-PLAN.md), aber auf 15 Minuten gekürzt. Die Prompt-Dateien liegen in [prompts/](prompts/README.md).

**Was gegenüber dem Live-Plan wegfällt:**

- Schritt 0 läuft vor dem Vortrag.
- Kein RACI-Negativtest (nur erwähnen).
- In Schritt 03 kein zweiter Skill-Lauf. Das Memory aus Schritt 02 bleibt, nur der Wochenbericht wird als PDF erzeugt.
- In Schritt 04 keine Duplikat-Probe (nur erwähnen).
- Schritt 05 wird nicht live gebaut. Die fertigen Dateien kommen aus dem Referenz-Branch, gezeigt wird nur der 5-Sekunden-Check.

**Grundregel für Wartezeiten:** Während ein Bau-Prompt läuft (40 s bis 2 min), erklärst du, was gerade entsteht. Dafür sind die Sprechzeilen unten da.

---

## Vorher (vor dem Vortrag, nicht auf der Uhr)

```bash
cd ~/Documents/projects/Agent-Template
git switch demo/01-ai-hub
git branch -D demo/live 2>/dev/null; git switch -c demo/live
DEMO_GH_REPO=a-lottes/Agent-Template demo/setup-workspace.sh
```

Zwei Fenster nebeneinander öffnen und in beiden `claude` starten:

| Links: Repo-Session | Rechts: Demo-Session |
|---|---|
| `cd ~/Documents/projects/Agent-Template && claude` | `cd ~/agent-demo && claude` |

Ein Terminal-Tab bleibt frei für die Setup-Befehle. Dazu den Browser-Tab `github.com/a-lottes/Agent-Template/issues` öffnen.

---

## Ablauf

| Zeit | Schritt | Fenster | Aktion |
|---|---|---|---|
| 0:00 | Einstieg | – | *„Wohin gehen die Daten? Und wie passt man einen Skill an?“* |
| 0:30 | **01 Hub** | rechts | `/provider adesso-hub` → `/exit` → `claude -c` → `/status` |
| 1:30 | | rechts | `Führe @project-memory/docs/demo/prompts/01-demo-summary.md aus.` (ca. 10 s) |
| 2:00 | | rechts | `/provider anthropic` → `/exit` → `claude -c` |
| 2:30 | **02 Skill** | links | `Führe @docs/demo/prompts/02-build.md aus.` (ca. 40 s) |
| | | | *Erklären: Beschreibung = Schnittstelle, Anleitung = Implementierung, Tabellen im Skill.* |
| 3:30 | | Terminal | `demo/setup-workspace.sh --plugin-only` |
| | | rechts | `/exit` → `claude` |
| 4:00 | | rechts | `Führe @project-memory/docs/demo/prompts/02-demo-skill.md aus.` (ca. 70 s) |
| | | | *Erklären: Skill löst aus, drei Subagents mit drei Modellen, Reviewer prüft gegen die Quelle.* |
| 5:30 | | rechts | `memory/actions.md` zeigen: Ben `2026-10-19`, Cleanup `TBD` |
| 6:00 | **03 PDF** | links | `Führe @docs/demo/prompts/03-build.md aus.` (ca. 2 min) |
| | | | *Erklären: Layout gehört in ein Skript, das Modell entscheidet nur, wann es läuft.* |
| 8:00 | | Terminal | `demo/setup-workspace.sh --plugin-only` (`memory/` bleibt) |
| | | rechts | `/exit` → `claude` |
| 8:15 | | rechts | `/project-memory:weekly-status` (ca. 20 s) |
| 8:45 | | Terminal | `open ~/agent-demo/memory/status-draft.pdf` |
| 9:15 | **04 GitHub** | links | `Führe @docs/demo/prompts/04-build.md aus.` (ca. 50 s) |
| | | | *Erklären: nur auf Wunsch, erst Vorschau, keine Duplikate.* |
| 10:15 | | Terminal | `demo/setup-workspace.sh --plugin-only` |
| | | rechts | `/exit` → `claude` (neue Sitzung, nicht `-c`) |
| 10:30 | | rechts | `Führe @project-memory/docs/demo/prompts/04-demo-issues.md aus.` → Vorschau |
| 11:00 | | rechts | `Ja, bitte anlegen.` → Issues im Browser zeigen |
| 12:00 | **05 Prüfen** | Terminal | siehe unten (ca. 15 s) |
| 13:00 | Fazit | – | *„Skill = Anleitung wie Code: einsetzen, erweitern, prüfen. Motor wählbar.“* |
| 13:30 | Puffer | – | 1,5 Minuten Reserve |

### Schritt 05 im Terminal

```bash
cd ~/Documents/projects/Agent-Template
git checkout demo/05-skill-check -- evals scripts/eval.sh scripts/skill_check.py
git commit -qm "Demo 05: Validierung und Eval-Fälle (aus Referenz)"
claude plugin validate --strict skills
scripts/eval.sh adesso-hub --case no-trigger
```

*„Die Eval-Fälle habe ich vorbereitet. Der Kurz-Eval läuft souverän über den Hub, in drei Sekunden und kostenlos. Im Team läuft das bei jeder Skill-Änderung in der CI.“*

Optional `evals/no-trigger/case.yaml` 15 Sekunden lang zeigen.

---

## Wenn es eng wird

| Lage | Kürzung |
|---|---|
| Nach Schritt 02 schon über 6:30 | Schritt 03 nur zeigen statt bauen: `git checkout demo/03-skill-pdf -- skills commands .claude-plugin && git commit -qm "Demo 03 (Referenz)"`, dann weiter wie in der Tabelle |
| Nach Schritt 03 schon über 10:00 | Schritt 04 ebenso aus der Referenz holen (`demo/04-skill-github`), nur Vorschau zeigen, nicht anlegen |
| Ein Bau-Prompt hängt | Abbrechen (Esc), Dateien aus dem Referenz-Branch holen (wie oben), weiter |
| Hub antwortet nicht | Schritt 01 nur mit `/provider` (Tabelle) zeigen, nicht umschalten |

Nach dem Vortrag: [prompts/99-after-demo.md](prompts/99-after-demo.md) und die Demo-Issues schließen.
