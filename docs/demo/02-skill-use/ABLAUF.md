# 02 · Skill bauen: Aufgaben aus Notizen und Todos (Detail)

Teil von [ANLEITUNG.md](../ANLEITUNG.md), Schritt 2. Bau-Prompt: [prompts/02-build.md](../prompts/02-build.md). Referenzstand: Branch `demo/02-skill-use`.

## Botschaft

> „Ein Skill ist eine Anleitung mit einer Schnittstelle. Die Beschreibung entscheidet, *ob* er geladen wird, der Inhalt, *wie* gearbeitet wird.“

## Was der Bau-Prompt ändert

| Datei | Änderung |
|---|---|
| `.claude-plugin/marketplace.json` | neu: das Repo ist zugleich Marketplace |
| `.claude-plugin/plugin.json` | Version 0.2.0 |
| `skills/meeting-to-actions/SKILL.md` | Beschreibung mit deutschen Auslösern und Todos; Subagents mit Präfix und im Vordergrund; Tabellen direkt im Skill; Regeln für ISO-Datum, vage Aussagen und diktierte Todos |
| `agents/action-extractor.md`, `agents/reviewer.md` | Hedged-Regel, ISO-Datum |
| `skills/meeting-to-actions/templates/` | gelöscht (Inhalt steht jetzt im Skill) |

Am Ende registriert Claude das Plugin für den Repo-Ordner (`claude plugin marketplace add . --scope local`, `claude plugin install project-memory@adesso-agent-demo --scope local`). In jeder neuen Session ist der Skill dann verfügbar.

## Was zu zeigen ist

In VS Code unter Source Control den Diff des Schritts (die Bau-Prompts committen nicht).

`skills/meeting-to-actions/SKILL.md`:
- Frontmatter: *„Das ist die Schnittstelle. Nur diese Zeilen kennt Claude dauerhaft.“*
- Prozedur: *„Das ist die Implementierung. Sie wird erst geladen, wenn die Beschreibung passt.“*
- Regel „diktierte Todos“: Notiz wird in `inbox/` abgelegt und durchläuft denselben Weg wie ein Protokoll.

## Benutzen

- [prompts/02-demo-todos.md](../prompts/02-demo-todos.md): drei Todos, davon eines mit „Vielleicht“. Erwartet werden `Skill(project-memory:meeting-to-actions)`, drei Subagents (Triage, Extraktion, Review) und Einträge in `memory/actions.md`. Das „Vielleicht“ wird keine feste Aufgabe.
- `/actions`: offene Aufgaben als Tabelle.
- Optional [prompts/02-demo-skill.md](../prompts/02-demo-skill.md): das Steering-Protokoll aus `inbox/` verarbeiten.

## Regeln für gute Skills

1. Eine Aufgabe pro Skill.
2. Die Beschreibung sagt, *wann* (echte Auslöser, auch deutsch).
3. Die Anleitung besteht aus nummerierten Schritten, die Regeln sind harte Verbote.
4. Das Format steht im Skill, nicht in einer Datei, die headless eventuell nicht lesbar ist.
5. Abhängigkeiten werden eindeutig benannt (`project-memory:reviewer`).
6. Kein `allowed-tools` im Frontmatter. Damit wurde der Skill in Tests nicht geladen.
7. Vor dem Verteilen validieren: `claude plugin validate --strict skills`.
