# 04 · Von der Notiz ins Ticketsystem (visuell)

## Die Idee

Aufgaben aus dem Meeting landen nicht nur in einer Datei, sondern auf Wunsch als Issues in GitHub. Ein Mensch bestätigt, bevor etwas angelegt wird.

```mermaid
flowchart LR
    MEM["📝 memory/actions.md<br/>offene Aufgaben"] --> PRE["👀 Vorschau<br/>--dry-run"]
    PRE --> OK{"🙋 Mensch:<br/>„ja“?"}
    OK -->|ja| GH["🐙 gh issue create"]
    OK -->|nein| STOP["⏹️ nichts passiert"]
    GH --> ISS["✅ GitHub-Issues<br/>#1 #2 #3"]
    GH --> BACK["✍️ actions.md<br/>Status: open · #1"]

    style PRE fill:#fff8c5,stroke:#9a6700
    style OK fill:#ddf4ff,stroke:#0969da
    style ISS fill:#dafbe1,stroke:#1a7f37
```

## Die Änderung im Skill

```mermaid
flowchart TB
    subgraph SKILL["SKILL.md · v0.4.0"]
        D["description:<br/>+ „…should become GitHub issues“<br/>+ „Issues/Tickets anlegen“"]
        P["Procedure 1–7<br/><i>unverändert</i>"]
        L["<b>NEU: Later: action items as GitHub issues</b><br/>1. Vorschau zeigen, fragen<br/>2. nach „ja“ anlegen<br/>3. PDFs neu erzeugen"]
    end
    style L fill:#dafbe1,stroke:#1a7f37
    style D fill:#dafbe1,stroke:#1a7f37
```

> Die Beschreibung bekommt neue Auslöser, damit der Skill bei „Tickets anlegen“ anspringt. Der neue Abschnitt sagt, *wie*.

## Ablauf live

```mermaid
sequenceDiagram
    autonumber
    actor Jan
    participant CC as Claude Code
    participant PY as create_issues.py
    participant GH as GitHub
    participant MEM as actions.md

    Jan->>CC: „Lege für die offenen Aufgaben GitHub-Issues an.“
    CC->>PY: --dry-run
    PY-->>CC: 3 Issues würden angelegt
    CC-->>Jan: Vorschau · „Soll ich?“
    Jan->>CC: ja
    CC->>PY: anlegen
    PY->>GH: gh issue create (×3)
    GH-->>PY: #1 #2 #3
    PY->>MEM: Status: open · #1 …
    CC-->>Jan: Links zu den Issues
    Jan->>CC: nochmal
    CC-->>Jan: „Nothing to do“ (keine Duplikate)
```

## Drei Sicherheitsgurte

```mermaid
flowchart LR
    A["🙋 Nur auf Wunsch<br/>kein Auto-Anlegen"] --> B["👀 Erst Vorschau<br/>dann Bestätigung"] --> C["🔁 Idempotent<br/>keine Duplikate"]
    style A fill:#ddf4ff
    style B fill:#fff8c5
    style C fill:#dafbe1
```

## Der ganze Weg einer Aufgabe

```mermaid
flowchart LR
    P["📥 Protokoll"] --> S["🧩 Skill"] --> M["📝 actions.md"] --> F["📄 actions.pdf"]
    M --> I["🐙 GitHub-Issue"]
    I --> T["👩‍💻 Team arbeitet daran"]
```

## Kernaussage

> **Ein paar Zeilen im Skill, und der Agent reicht Arbeit ins Ticketsystem weiter, mit Vorschau, Bestätigung und ohne Duplikate.**
