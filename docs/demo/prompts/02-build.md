# Schritt 02 · Bau-Prompt: Skill einsetzen (Repo-Session)

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
   - Wichtig: Frontmatter nur name und description, kein allowed-tools (damit wird der Skill nicht geladen).
6. Lösche skills/meeting-to-actions/templates/ (actions.md, decisions.md, risks.md).

Danach: claude plugin validate --strict skills und claude plugin validate --strict agents ausführen und Ergebnis zeigen. Zum Schluss committen: "Demo 02: Skill einsetzen (Marketplace, Tabellen im Skill, Hedged-Regel)".
