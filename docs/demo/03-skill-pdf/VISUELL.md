# 03 · Aus Notizen werden Dokumente (visuell)

## Die Idee

Der Skill schreibt seine Ergebnisse wie bisher als Markdown. Mit einer kleinen Anpassung legt er jedes Ergebnis zusätzlich als PDF daneben, fertig zum Verschicken.

```mermaid
flowchart LR
    IN["📥 Protokoll<br/>inbox/"] --> SK["🧩 Skill<br/>meeting-to-actions"]
    SK --> MD["📝 Markdown<br/>actions · decisions · risks"]
    MD --> PY["⚙️ md_to_pdf.py<br/><i>immer gleiches Layout</i>"]
    PY --> PDF["📄 PDF<br/>daneben gespeichert"]
    MD -.->|"Quelle, versioniert"| GIT[("🗂️ Git")]
    PDF -.->|"Lieferobjekt"| MAIL["✉️ Steering-Komitee"]

    style MD fill:#ddf4ff,stroke:#0969da
    style PDF fill:#ffebe9,stroke:#cf222e
    style PY fill:#fff8c5,stroke:#9a6700
```

## Die ganze Änderung: zwei Zeilen

```mermaid
flowchart TB
    subgraph VORHER["SKILL.md · vorher"]
        V5["5. processed.md aktualisieren"]
        V6["6. Zusammenfassen"]
    end
    subgraph NACHHER["SKILL.md · nachher"]
        N5["5. processed.md aktualisieren"]
        N6["<b>6. Jede Datei als PDF daneben speichern</b><br/>python3 ${CLAUDE_SKILL_DIR}/scripts/md_to_pdf.py memory"]
        N7["7. Zusammenfassen"]
    end
    VORHER ==>|"+ 2 Zeilen<br/>+ 1 Skript"| NACHHER
    style N6 fill:#dafbe1,stroke:#1a7f37
```

## Wer macht was?

```mermaid
flowchart LR
    M["🤖 Modell<br/>entscheidet <b>wann</b>"] --> S["⚙️ Skript<br/>entscheidet <b>wie</b>"]
    S --> R["📄 jedes Mal<br/>gleiches PDF"]
```

> **Faustregel:** Was immer gleich aussehen muss (Layout, Format, Berechnung), gehört in ein Skript. Das Modell ruft es nur auf.

## Was am Ende in `memory/` liegt

```mermaid
flowchart LR
    subgraph MEM["📁 memory/"]
        direction TB
        A1["actions.md"] --- A2["actions.pdf"]
        D1["decisions.md"] --- D2["decisions.pdf"]
        R1["risks.md"] --- R2["risks.pdf"]
        S1["status-draft.md"] --- S2["status-draft.pdf"]
    end
    style A2 fill:#ffebe9
    style D2 fill:#ffebe9
    style R2 fill:#ffebe9
    style S2 fill:#ffebe9
```

## Ablauf live

```mermaid
sequenceDiagram
    autonumber
    actor Jan
    participant CC as Claude Code
    participant SK as Skill
    participant PY as md_to_pdf.py
    participant MEM as memory/

    Jan->>CC: „Projektgedächtnis aktualisieren“
    CC->>SK: Skill laden (v0.3.0)
    SK->>MEM: actions.md · decisions.md · risks.md
    SK->>PY: Schritt 6: PDFs erzeugen
    PY->>MEM: actions.pdf · decisions.pdf · risks.pdf
    Jan->>CC: /project-memory:weekly-status
    CC->>MEM: status-draft.md + status-draft.pdf
```

## Kernaussage

> **Ein Skill ist eine Anleitung, also lässt er sich wie eine Anleitung erweitern.** Zwei Zeilen plus ein Skript, und aus Notizen werden verschickbare Dokumente.
