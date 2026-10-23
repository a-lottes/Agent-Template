# 00 · Worum geht es? (visuell)

## Die Idee in einem Bild

Wir behalten den Agenten aus Teil 1 und zeigen, wie man seinen wichtigsten Baustein, den **Skill**, einsetzt und mit kleinen Änderungen erweitert. Den Motor (das Modell) können wir dabei frei wählen.

```mermaid
flowchart LR
    A["🔌 Modell wählen<br/>adesso AI Hub<br/>oder Anthropic"] --> B["🧩 Skill einsetzen"]
    B --> C["📄 Anpassen 1<br/>Markdown + PDF"]
    C --> D["🐙 Anpassen 2<br/>GitHub-Issues"]
    D --> E["✅ Prüfen<br/>validate + Kurzlauf"]

    style A fill:#1f6feb,color:#fff,stroke:#1f6feb
    style B fill:#8957e5,color:#fff,stroke:#8957e5
    style C fill:#db6d28,color:#fff,stroke:#db6d28
    style D fill:#24292f,color:#fff,stroke:#24292f
    style E fill:#2da44e,color:#fff,stroke:#2da44e
```

## Ein Ordner, ein Branch, vier Schritte

Live gebaut wird auf einem Branch `demo/live`. Die fertigen Stände der Schritte liegen als Referenz in eigenen Branches bereit.

```mermaid
gitGraph
    commit id: "main: Plugin aus Teil 1"
    branch demo/01-ai-hub
    commit id: "Startpunkt"
    branch demo/live
    commit id: "Demo 02: Skill"
    commit id: "Demo 03: PDF"
    commit id: "Demo 04: GitHub"
```

## Der Arbeitsplatz

Alles passiert im Repo-Ordner. Eingaben landen in `inbox/`, Ergebnisse in `memory/`. Beide Ordner sind von Git ausgeschlossen.

```mermaid
flowchart TB
    subgraph REPO["📁 Repo-Ordner"]
        SK["🧩 skills/meeting-to-actions<br/>der Skill, den wir bauen"]
        IN["📥 inbox/<br/>Protokolle, diktierte Todos"]
        MEM["🧠 memory/<br/>actions · decisions · risks (+ PDF)"]
        CFG["⚙️ .claude/<br/>/provider · /actions · Provider-Profil"]
    end
    U(["👤 Prompt oder Todos"]) --> AG(("🤖 Claude Code"))
    SK --> AG
    IN --> AG
    AG -->|schreibt| MEM
    AG -.->|auf Wunsch| GH["🐙 GitHub-Issues"]
```

## Ablauf über 15 Minuten

```mermaid
timeline
    title Live-Demo BL-AT 2026
    0-2 min   : AI Hub zeigen : /provider
    2-6 min   : Skill bauen : Todos eintragen : /actions
    6-10 min  : Skill erweitern : PDF
    10-14 min : Skill erweitern : GitHub-Issues
    14-15 min : Fazit
```

## Kernaussage

> **Ein Skill ist eine Anleitung, die man wie Code behandelt.** Ein paar Zeilen mehr, und aus Markdown-Notizen werden PDF-Berichte und GitHub-Issues. Validieren und kurz prüfen gehört dazu.
