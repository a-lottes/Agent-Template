# 01 · adesso AI Hub zeigen, `/provider` zum Umschalten (Detail für Jan)

Branch: `demo/01-ai-hub` · baut auf `demo/00-setup` auf · Dauer live: ca. 3 Minuten

## Botschaft

> „Der Motor ist austauschbar, das Auto bleibt. Ein Befehl in Claude Code, und derselbe Agent läuft auf souveränen Modellen im adesso AI Hub. Für den Rest der Demo nehmen wir die Original-Claude-Modelle, weil sie schneller und zuverlässiger sind.“

Der Hub wird **gezeigt**, nicht durchgängig benutzt. Ab Schritt 02 läuft alles mit `anthropic`.

## Was in diesem Branch dazukommt

| Datei | Zweck |
|---|---|
| `providers/anthropic.json` | Profil „Original“: setzt alle Hub-Variablen leer, nutzt deinen Claude-Login |
| `providers/adesso-hub.json` | Profil „souverän“: Hub-URL, drei Modell-Aliase auf kostenlose Hub-Modelle |
| `providers/adesso-hub-claude.json` | Profil „Claude über den Hub“, sobald euer Key dafür freigeschaltet ist |
| `demo/workspace/.claude/commands/provider.md` | **Slash-Befehl `/provider`** im Workspace |
| `scripts/provider.sh` (+ `provider.py`) | Umschalten: `provider.sh adesso-hub`, `provider.sh anthropic`, `provider.sh` (Status) |
| `scripts/hub-key.sh` | `apiKeyHelper`: Key aus Schlüsselbund oder `$ADESSO_AI_HUB_KEY`, nie im Klartext in Dateien |
| `scripts/model_check.py` | Testet jedes Hub-Modell: erreichbar? schnell? ruft es Tools korrekt auf? |
| `copilot/chatLanguageModels.adesso-hub.json` | Vorlage für GitHub Copilot (ohne Key) |
| `demo/setup-workspace.sh` | kopiert `/provider`, legt `.claude/providers/*.json` und VS-Code-Tasks an, Standard-Profil `anthropic` |

## Drei Wege zum Umschalten

| Weg | Befehl | Wann |
|---|---|---|
| **In Claude Code** (empfohlen) | `/provider adesso-hub` → `/exit` → `claude -c` | live auf der Bühne, Gespräch läuft weiter. Verfügbar in `~/agent-demo` **und** im Repo-Ordner |
| Einmalig, ohne umzuschalten | `claude --settings .claude/providers/adesso-hub.json` | „nur mal kurz zeigen“ |
| VS Code ohne Terminal | *Terminal → Run Task… → Provider: …* | für Kolleg:innen, die nicht tippen wollen |

Warum ein Neustart nötig ist: Der Provider (Adresse und Key) gehört zur Sitzung. `/model` wechselt nur das Modell **innerhalb** eines Providers. `claude -c` setzt dasselbe Gespräch fort, getestet: Die Session-ID bleibt gleich, Claude kennt danach den bisherigen Verlauf.

So funktioniert `/provider` technisch: Der Befehl **merkt den Wechsel nur vor** (`.claude/settings.local.json.next`) und bestätigt noch auf dem alten Provider. Beim `/exit` aktiviert ein `SessionEnd`-Hook (in `.claude/settings.json`, angelegt von `setup-workspace.sh`) die neue Datei. Hintergrund aus der Generalprobe: Schreibt man die Settings sofort, lädt Claude Code sie noch während der laufenden Antwort nach und schickt diese mit dem alten Modell an den neuen Provider. Das ergibt eine Fehlermeldung.

Mehrere Provider in **einer** Settings-Datei gleichzeitig gehen nicht: Claude Code kennt pro Sitzung genau eine `ANTHROPIC_BASE_URL`. Deshalb ein Profil pro Provider.

### Was hinter den drei Modellen steckt

| Alias | Rolle im Plugin | `anthropic` | `adesso-hub` | `adesso-hub-claude` |
|---|---|---|---|---|
| `opus` | `reviewer` | Claude Opus | `deepseek-v4-flash-sovereign` | `claude-opus-5` |
| `sonnet` | Hauptsession, `action-extractor` | Claude Sonnet | `deepseek-v4-flash-sovereign` | `claude-sonnet-5` |
| `haiku` | `doc-triage` | Claude Haiku | `qwen-3.6-35b-sovereign` | `claude-haiku-5` |

Gemessen am 20.10.2026: DeepSeek und Qwen rufen Tools korrekt auf (DeepSeek ca. 1,2 s, Qwen ca. 3,9 s). Claude über den Hub: `key_model_access_denied` für den verwendeten Key. Ein voller Skill-Lauf dauert auf Hub und Anthropic gleich lang (ca. 2 min), die Ergebnisqualität ist mit Claude aber deutlich besser.

## Vorbereitung (einmalig)

```bash
cd ~/Documents/projects/Agent-Template
git switch demo/01-ai-hub
scripts/provider.sh set-url https://<ai-hub-host>   # Hub-Adresse, nur lokal (providers/.hub-url, gitignored)
scripts/provider.sh set-key          # Hub-Key in den Schlüsselbund (Eingabe verdeckt)
scripts/model_check.py               # Hub-Modelle testen
demo/setup-workspace.sh              # Workspace inkl. /provider, Standard: anthropic
```

**Pflicht:** Einen eventuellen Alias `alias claude="… --settings …"` (z. B. in `~/.zshrc`) auskommentieren und eine neue Shell öffnen. Sonst gewinnt immer die Hub-Datei aus dem Alias und `/provider` wirkt nicht. Notlösung: `command claude` tippen.

**Copilot:** Custom-Endpoint einmalig einrichten: VS Code → Modellauswahl im Chat → *Manage Models…* → *Add Models* → Custom Endpoint (Chat Completions), URL `https://<ai-hub-host>/v1/chat/completions`, Modelle wie in `copilot/chatLanguageModels.adesso-hub.json`. Den Key im Dialog eingeben.

## Live-Ablauf

### 1 · Profil zeigen (45 s)

`providers/adesso-hub.json` in VS Code öffnen, drei Stellen zeigen:

- `ANTHROPIC_BASE_URL`: *„Hier biegen wir ab. Der Hub spricht dieselbe API wie Anthropic.“*
- `ANTHROPIC_DEFAULT_*_MODEL`: *„Die Subagents heißen haiku, sonnet, opus. Diese drei Zeilen legen fest, welches Hub-Modell dahintersteckt.“*
- `apiKeyHelper`: *„Kein Key in der Datei, er kommt aus dem Schlüsselbund.“*

### 2 · Umschalten in Claude Code (90 s)

```bash
cd ~/agent-demo
claude
```

In Claude Code:

```
/provider adesso-hub
/exit
```

```bash
claude -c
```

```
/status                          ← zeigt die Hub-Adresse
Fasse inbox/2026-10-12-steering.md in drei Stichpunkten zusammen.
```

*„Gleicher Agent, gleiches Gespräch, souveränes Modell.“*

### 3 · Zurück zum Original (30 s)

```
/provider anthropic
/exit
```

```bash
claude -c
```

*„Für den Rest nehmen wir die Original-Modelle, die sind für Agenten-Läufe am stärksten.“*

### 4 · Copilot (30 s)

Copilot-Chat öffnen, Modellauswahl aufklappen: oben die Copilot-Modelle (u. a. Claude), darunter „Adesso AI Hub“ mit DeepSeek und Qwen. *„Gleicher Hub, zweites Werkzeug, Wechsel per Dropdown.“*

## Plan B

| Problem | Ausweg |
|---|---|
| `/provider` unbekannt | Claude im falschen Ordner gestartet. `/provider` ist ein Projekt-Befehl und existiert nur in `~/agent-demo` (nach `demo/setup-workspace.sh`) und im Repo-Ordner ab Branch `demo/01-ai-hub`. In VS Code den passenden Ordner öffnen. Notlösung im Terminal: `project-memory/scripts/provider.sh adesso-hub` |
| Nach `/exit` + `claude -c` noch alter Provider | Vertrauensdialog nicht bestätigt (Hook lief nicht) → im Terminal `project-memory/scripts/provider.sh adesso-hub`, dann `claude -c` |
| `/status` zeigt trotzdem den Hub nach `/provider anthropic` | Alias aktiv → `command claude -c` |
| `No AI Hub key found` | `scripts/provider.sh set-key` |
| Hub antwortet nicht | Teil überspringen, Screenshot zeigen, weiter mit Schritt 02 |
| VS Code nutzt alten Provider | neue Claude-Session öffnen |

## Mögliche Fragen

- **Geht noch etwas zu Anthropic?** Im Hub-Profil nicht: Modellaufrufe gehen an den Hub, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` schaltet Telemetrie und Auto-Update ab.
- **Warum nicht global umstellen?** Weil dann alle Projekte umgestellt sind. Profil pro Workspace ist gezielt und nachvollziehbar.
- **Windows?** Gleiche Profile. Key per `setx ADESSO_AI_HUB_KEY "<key>"`, `apiKeyHelper` im Profil auf `powershell -c "$env:ADESSO_AI_HUB_KEY"` ändern.
