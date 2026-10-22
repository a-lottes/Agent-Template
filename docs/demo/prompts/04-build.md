# Schritt 04 · Bau-Prompt: Aufgaben als GitHub-Issues (Repo-Session)

Baue Schritt 04 auf demo/live, ohne Merge. Ziel:

1. Neu: skills/meeting-to-actions/scripts/create_issues.py (ausführbar mit chmod +x, Standardbibliothek plus gh CLI).
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

Test im Ordner .scratch/ im Repo (ist per .gitignore ausgeschlossen, nicht /tmp): Lege .scratch/actions.md mit einer Tabelle | Action | Owner | Due | Status | Source | an (zwei Zeilen open, eine Zeile "open · #7"). Führe create_issues.py .scratch/actions.md --repo a-lottes/Agent-Template --dry-run aus. Erwartet: zwei Issues in der Vorschau, die Zeile mit #7 wird übersprungen. Kein echtes Anlegen, kein Aufruf ohne --dry-run. Danach .scratch/ löschen.

Zum Schluss committen: "Demo 04: Action items als GitHub-Issues". Der Working Tree muss danach sauber sein (git status).
