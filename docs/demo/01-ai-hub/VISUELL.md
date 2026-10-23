# 01 · Gleicher Agent, anderer Motor (visuell)

## Die Idee

Claude Code ist das Auto, das Modell ist der Motor. Mit dem adesso AI Hub tauschen wir den Motor gegen einen souveränen, ohne am Auto etwas zu ändern.

```mermaid
flowchart LR
    subgraph LAPTOP["💻 Laptop"]
        CC["Claude Code<br/>+ Plugin · Skill · Hooks"]
        GH["GitHub Copilot<br/>in VS Code"]
    end

    subgraph HUB["🏢 adesso AI Hub"]
        GW["Gateway<br/>Auth · Budget · Logging · Routing"]
        DS["DeepSeek V4 Flash<br/>souverän (nicht im Profil)"]
        QW["Qwen 3.6 35B<br/>souverän"]
        CL["Claude-Modelle<br/>(nach Freischaltung)"]
    end

    ANT["☁️ Anthropic<br/>Original"]

    CC -- "Profil: adesso-hub" --> GW
    GH -- "Modellauswahl" --> GW
    CC -. "Profil: anthropic" .-> ANT
    GH -. "Copilot-Modelle" .-> ANT
    GW --> DS
    GW --> QW
    GW -.-> CL

    style HUB fill:#e8f1ff,stroke:#1f6feb
    style ANT fill:#fff4e5,stroke:#db6d28
```

## Ein Befehl zum Umschalten, direkt in Claude Code

```mermaid
sequenceDiagram
    autonumber
    actor Jan
    participant CC as Claude Code
    participant P as /provider
    participant S as .claude/settings.local.json

    Jan->>CC: /provider adesso-hub
    CC->>P: Skript ausführen
    P->>S: Profil „adesso-hub“ vormerken (.next)
    P-->>Jan: Tabelle: Hub · Qwen
    Jan->>CC: neue Session (CLI: /exit, claude -c)
    Note over CC: neuer Provider aktiv
    Jan->>CC: /status → AI Hub ✅
```

```mermaid
flowchart LR
    A["anthropic<br/>☁️ Claude-Login"] <-->|"/provider"| H["adesso-hub<br/>🏢 souverän"]
    H <-->|"/provider"| HC["adesso-hub-claude<br/>🏢 Claude im Hub"]
    style A fill:#fff4e5,stroke:#db6d28
    style H fill:#e8f1ff,stroke:#1f6feb
    style HC fill:#e8f1ff,stroke:#1f6feb,stroke-dasharray: 5 5
```

> Warum eine neue Session? Adresse und Key gelten pro Sitzung. In VS Code einfach eine neue Session öffnen. In der CLI `/exit` und `claude -c`, dann läuft das Gespräch weiter.

## Drei Namen, beliebige Modelle

Das Plugin kennt nur die Rollen-Namen `opus`, `sonnet`, `haiku`. Das Profil entscheidet, welches echte Modell antwortet.

```mermaid
flowchart LR
    subgraph PLUGIN["🧩 Plugin (bleibt unverändert)"]
        T["doc-triage<br/>model: haiku"]
        E["action-extractor<br/>model: sonnet"]
        R["reviewer<br/>model: opus"]
    end

    subgraph SOUV["Profil adesso-hub"]
        Q["Qwen 3.6 35B"]
        D1["Qwen 3.6 35B"]
        D2["Qwen 3.6 35B"]
    end

    subgraph ORIG["Profil anthropic"]
        H["Claude Haiku"]
        S["Claude Sonnet"]
        O["Claude Opus"]
    end

    T --> Q
    E --> D1
    R --> D2
    T -.-> H
    E -.-> S
    R -.-> O
```

## Erst messen, dann einsetzen

Bevor ein Modell in den Agenten darf, prüfen wir: Ist es erreichbar, ist es schnell, ruft es Werkzeuge richtig auf?

```mermaid
xychart-beta
    title "Antwortzeit Tool-Call-Test (Sekunden, kleiner ist besser)"
    x-axis ["DeepSeek V4 Flash", "Qwen 3.6 35B"]
    y-axis "Sekunden" 0 --> 5
    bar [1.2, 3.9]
```

| Modell | erreichbar | Tool-Call korrekt | Rolle |
|---|---|---|---|
| DeepSeek V4 Flash | ✅ API · ⚠️ in Claude Code unzuverlässig | ✅ | nicht im Profil |
| Qwen 3.6 35B | ✅ | ✅ | alle Rollen (opus · sonnet · haiku) |
| Claude über den Hub | ⛔ noch nicht freigeschaltet | – | später Vergleich |

## Was bei einer Anfrage passiert

```mermaid
sequenceDiagram
    autonumber
    actor Jan
    participant CC as Claude Code
    participant KC as Schlüsselbund
    participant HUB as adesso AI Hub
    participant M as Qwen 3.6 (souverän)

    Jan->>CC: „Verarbeite die Inbox“
    CC->>KC: apiKeyHelper: Key holen
    KC-->>CC: Key (nie in einer Datei)
    CC->>HUB: Anfrage im Anthropic-Format
    HUB->>HUB: Key prüfen · Budget · Log
    HUB->>M: weiterleiten
    M-->>HUB: Antwort + Tool-Aufrufe
    HUB-->>CC: Antwort
    CC-->>Jan: Ergebnis in memory/
```

## Kernaussage

> **Ein Befehl hin, ein Befehl zurück.** Plugin, Skill und Hooks bleiben gleich, nur der Motor wechselt. Wir zeigen den Hub und arbeiten danach mit den Original-Claude-Modellen weiter.
