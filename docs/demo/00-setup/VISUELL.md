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

## Sechs Branches, eine Treppe

Jede Stufe baut auf der vorherigen auf. Klappt live etwas nicht, nehmen wir einfach die nächste Stufe.

```mermaid
gitGraph
    commit id: "main: Plugin aus Teil 1"
    branch demo/00-setup
    commit id: "Demo-Workspace"
    branch demo/01-ai-hub
    commit id: "/provider"
    branch demo/02-skill-use
    commit id: "Skill einsetzen"
    branch demo/03-skill-pdf
    commit id: "MD + PDF"
    branch demo/04-skill-github
    commit id: "GitHub-Issues"
    branch demo/05-skill-check
    commit id: "Prüfen"
```

## Der Demo-Arbeitsplatz

Ein Ordner auf dem Laptop. Das Setup-Skript kopiert das Plugin des aktuellen Git-Branches hinein, so ist jeder Demo-Schritt mit einem Befehl hergestellt.

```mermaid
flowchart TB
    subgraph WS["📁 ~/agent-demo"]
        IN["📥 inbox/<br/>Meeting-Protokoll"]
        MEM["🧠 memory/<br/>decisions · actions · risks"]
        CM["📄 CLAUDE.md<br/>Projektkontext"]
        ST["⚙️ .claude/<br/>Einstellungen & Provider"]
        PL["📦 project-memory<br/>(Kopie aus dem Repo)"]
    end
    REPO[("🗂️ Git-Repo<br/>aktueller Branch")] -.->|setup-workspace.sh| PL
    IN -->|Agent liest| AG(("🤖 Claude Code"))
    PL -->|Skill · Subagents · Hooks| AG
    AG -->|schreibt nur hierhin| MEM
```

## Ablauf über 20 Minuten

```mermaid
timeline
    title Live-Demo BL-AT 2026
    0-1 min   : Einstieg
    1-4 min   : AI Hub zeigen : /provider : Copilot
    4-8 min   : Skill einsetzen
    8-12 min  : Anpassen 1 : Markdown + PDF
    12-16 min : Anpassen 2 : GitHub-Issues
    16-19 min : Prüfen : validate + Kurzlauf
    19-20 min : Fazit : Q&A
```

## Kernaussage

> **Ein Skill ist eine Anleitung, die man wie Code behandelt.** Ein paar Zeilen mehr, und aus Markdown-Notizen werden PDF-Berichte und GitHub-Issues. Validieren und kurz prüfen gehört dazu.
