# Schritt 03 · Bau-Prompt: Markdown + PDF (Repo-Session)

Baue Schritt 03 auf demo/live, ohne Merge. Ziel:

1. Neu: skills/meeting-to-actions/scripts/md_to_pdf.py (ausführbar mit chmod +x, Python-Standardbibliothek, keine Abhängigkeiten).
   - Aufruf: md_to_pdf.py memory (alle *.md im Ordner, außer processed.md) oder md_to_pdf.py memory/actions.md (einzelne Datei). Ohne Argument: Hilfetext ausgeben.
   - Schreibt die PDF neben die .md (actions.md → actions.pdf) und gibt "<md> -> <pdf>" aus.
   - A4 Hochformat, Helvetica (Standard-Font, WinAnsi-Encoding), Kopfzeile "Project Memory · <Titel>" mit Datum, Seitenzahl "n / m" unten.
   - Unterstützt: Überschriften, Absätze, Aufzählungen (•), Zitate (grau, eingerückt), Pipe-Tabellen mit Kopfzeile in Fettschrift und Spaltenbreiten passend zum Text, Zeilenumbruch in Zellen. Inline-Markdown (**fett**, `code`, Links) als Klartext.
   - PDF von Hand schreiben (Objekte, xref, Trailer), ohne Bibliotheken.
   - Ein Dokumentationskopf mit den Aufrufbeispielen.
2. skills/meeting-to-actions/SKILL.md: Schritt 6 neu: Jede Memory-Datei als PDF neben das Markdown speichern, Aufruf python3 ${CLAUDE_SKILL_DIR}/scripts/md_to_pdf.py memory. Markdown bleibt die Quelle, PDFs nie von Hand bearbeiten. Danach ist Schritt 7 die Zusammenfassung. Kein allowed-tools im Frontmatter.
3. commands/weekly-status.md: description um "(Markdown and PDF)" ergänzen. Am Ende den Befehl python3 ${CLAUDE_PLUGIN_ROOT}/skills/meeting-to-actions/scripts/md_to_pdf.py memory/status-draft.md anhängen, mit dem Satz, dass die PDF neben dem Markdown gespeichert wird. Kein allowed-tools im Frontmatter.
4. .claude-plugin/plugin.json: version 0.2.0 → 0.3.0.

Test im Ordner .scratch/ im Repo (ist per .gitignore ausgeschlossen, nicht /tmp): Kopiere examples/inbox/2026-10-12-steering.md nicht, sondern lege dort ein kleines Test-Memory an (memory/actions.md mit einer Tabelle | Action | Owner | Due | Status | Source | und zwei Zeilen, dazu ein memory/status-draft.md mit Überschrift, Aufzählung, Zitat und Tabelle). Lass md_to_pdf.py auf .scratch/memory laufen, prüfe die PDFs mit file und zeig mir die Ausgabe. Danach .scratch/ löschen.

Zum Schluss committen: "Demo 03: Markdown + PDF-Export". Der Working Tree muss danach sauber sein (git status).
