# 04 · Skill erweitern: Aufgaben als GitHub-Issues (Detail)

Teil von [ANLEITUNG.md](../ANLEITUNG.md), Schritt 4. Bau-Prompt: [prompts/04-build.md](../prompts/04-build.md). Referenzstand: Branch `demo/04-skill-github`.

## Botschaft

> „Aufgaben, die nur in einer Datei stehen, werden vergessen. Auf Wunsch wandern sie als Issues nach GitHub, mit Vorschau und erst nach Bestätigung.“

## Was der Bau-Prompt ändert

| Datei | Änderung |
|---|---|
| `skills/meeting-to-actions/scripts/create_issues.py` | neu: liest `memory/actions.md`, legt per `gh issue create` Issues an, schreibt `#<nr>` in die Status-Spalte |
| `commands/create-issues.md` | neu: `/project-memory:create-issues` |
| `skills/meeting-to-actions/SKILL.md` | neuer Abschnitt „Later: action items as GitHub issues“, Auslöser „Issues/Tickets anlegen“ |
| `.claude-plugin/plugin.json` | Version 0.4.0 |

Zielrepo, in dieser Reihenfolge: `--repo`, dann `$PROJECT_MEMORY_GH_REPO`, dann die Zeile `GitHub repo for action items: owner/name` in `CLAUDE.md`, sonst **das GitHub-Repo des aktuellen Checkouts**. Im geklonten Repo landen die Issues also ohne weitere Konfiguration dort. Dafür braucht der Account Schreibrechte (`gh auth status`).

## Designentscheidungen

- **Nur auf Wunsch:** Ein normaler Skill-Lauf erzeugt nach außen nichts.
- **Erst Vorschau** (`--dry-run`), dann die Bestätigung durch den Menschen.
- **Idempotent:** Zeilen mit `#<nr>` werden übersprungen, es entstehen keine Duplikate.
- **`gh` statt eigener API:** Es wird die bestehende Anmeldung genutzt, kein Token in Dateien.

## Benutzen

1. [prompts/04-demo-issues.md](../prompts/04-demo-issues.md): Claude zeigt die Vorschau und fragt nach.
2. `Ja, bitte anlegen.`: Claude meldet die Issue-Links. In `memory/actions.md` steht `open · #<nr>`.
3. Im Browser die Issue-Liste des Repos zeigen.
4. Optional denselben Prompt noch einmal: „nichts Neues anzulegen“.

## Danach

[prompts/99-after-demo.md](../prompts/99-after-demo.md) listet die offenen Issues. Die Demo-Issues danach schließen.
