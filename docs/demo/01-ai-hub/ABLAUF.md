# 01 · adesso AI Hub zeigen und wechseln (Detail)

Teil von [ANLEITUNG.md](../ANLEITUNG.md), Schritt 1. Dauer ca. 2 Minuten.

## Botschaft

> „Der Motor ist austauschbar, das Auto bleibt. Ein Befehl, und derselbe Agent läuft auf souveränen Modellen im adesso AI Hub. Für die Agenten-Läufe der Demo nehmen wir danach die Anthropic-Modelle, weil sie dort deutlich schneller sind.“

## Was es dafür im Repo gibt

| Datei | Zweck |
|---|---|
| `automation/ai-hub/settings.example.json` | Beispiel-Konfiguration für Claude Code mit dem Hub |
| `providers/adesso-hub.json` | Profil „souverän“: alle drei Aliase auf `qwen-3.6-35b-sovereign` |
| `providers/anthropic.json` | Profil „Original“: leert alle Hub-Variablen, nutzt den Claude-Login |
| `providers/adesso-hub-claude.json` | Profil „Claude über den Hub“, sobald freigeschaltet |
| `scripts/provider.sh` | Umschalten, Hub-Adresse (`set-url`), Key (`set-key`) |
| `scripts/hub-key.sh` | `apiKeyHelper`: Key aus `$ADESSO_AI_HUB_KEY`, dem Schlüsselbund oder einer bestehenden Hub-Konfiguration in `~/.claude/settings.json` |
| `scripts/model_check.py` | Testet Hub-Modelle: erreichbar, schnell, Tool-Calls korrekt? |
| `copilot/chatLanguageModels.adesso-hub.json` | Vorlage für GitHub Copilot (Custom Endpoint) |

Die Hub-Adresse steht nicht im Repo: `scripts/provider.sh set-url https://<ai-hub-host>` legt sie lokal in `providers/.hub-url` ab (gitignored).

## Ablauf

1. `automation/ai-hub/settings.example.json` zeigen: `ANTHROPIC_BASE_URL`, die drei `ANTHROPIC_DEFAULT_*_MODEL`, `apiKeyHelper`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`.
2. `/provider adesso-hub` → **neue Session** → `/status` zeigt die Hub-Adresse.
3. Prompt direkt tippen: `Fasse inbox/2026-10-12-steering.md in drei Stichpunkten zusammen.` (Auf dem Hub lieber tippen als `@datei`, Qwen löst Dateiverweise langsamer auf.)
4. `/provider anthropic` → **neue Session**.

In der CLI statt „neue Session“: `/exit`, dann `claude -c`. Das Gespräch läuft weiter, ein Hook aktiviert den vorgemerkten Provider.

## Messwerte (Generalproben 20.–23.10.2026)

| Modell | Tool-Calls | Eindruck in Claude Code |
|---|---|---|
| Qwen 3.6 35B | ✓ | Einfache Fragen ok. Skill-Läufe mit Subagents teils über 6 Minuten, Bau-Prompts über 10 Minuten |
| DeepSeek V4 Flash | ✓ per API | In Claude Code unzuverlässig, nicht im Profil |
| Claude über den Hub | – | für den verwendeten Key nicht freigeschaltet |

## Copilot

VS Code → Modellauswahl im Chat → *Manage Models…* → *Add Models* → Custom Endpoint (Chat Completions), URL `https://<ai-hub-host>/v1/chat/completions`, Modelle wie in `copilot/chatLanguageModels.adesso-hub.json`.

## Plan B

| Problem | Ausweg |
|---|---|
| `apiKeyHelper`-Fehler | `scripts/provider.sh set-key` |
| `/status` zeigt nach `/provider anthropic` noch den Hub | Alias `claude --settings …` aktiv, entfernen |
| Hub antwortet nicht | Nur `/provider` (Tabelle) zeigen, nicht umschalten |
