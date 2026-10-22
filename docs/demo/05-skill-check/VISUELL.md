# 05 · Prüfen gehört dazu (visuell)

## Zwei Fragen, zwei Werkzeuge

```mermaid
flowchart LR
    S["🧩 Skill v0.4.0<br/>PDF + GitHub"] --> V{"✅ validate<br/><i>Ist er richtig gebaut?</i>"}
    V -->|ja| E{"📏 eval<br/><i>Tut er, was er soll?</i>"}
    E -->|grün| GO["🚀 an das Team verteilen"]
    E -->|rot| FIX["🛠️ Skill anpassen"]
    FIX --> V

    style V fill:#ddf4ff,stroke:#0969da
    style E fill:#fff8c5,stroke:#9a6700
    style GO fill:#dafbe1,stroke:#1a7f37
```

> **validate** = Linter: schnell, prüft nur die Form.
> **eval** = Test: lässt den Agenten echte Aufgaben lösen und prüft das Ergebnis.

## Ein Testfall auf einen Blick

```mermaid
flowchart TB
    P["💬 Prompt<br/>„What is a RACI matrix?“"] --> RUN["🤖 Claude Code<br/>mit Plugin"]
    RUN --> G1["🔎 Skill ausgelöst?<br/>soll: nein"]
    RUN --> G2["🔎 Frage beantwortet?<br/>soll: ja"]
    G1 & G2 --> SC(["Score 1.00 ✅"])
```

## Was der volle Check prüft

```mermaid
mindmap
  root((Skill-Check))
    steering-notes
      Skill löst aus
      Reviewer-Subagent genutzt
      Tabellenformat
      ISO-Datum
      PDF neben Markdown
    vague-owner
      „Probably Ben“ ist keine Zusage
    no-trigger
      Fremdfrage, Skill bleibt aus
```

## Ergebnis der Generalprobe

```mermaid
xychart-beta
    title "Skill-Check mit Claude: bestandene Prüfungen"
    x-axis ["steering-notes", "vague-owner", "no-trigger"]
    y-axis "Prüfungen" 0 --> 5
    bar [5, 2, 2]
```

**9 von 9 Prüfungen bestanden** · kurzer Lauf in Sekunden, voller Lauf ca. 2,5 Minuten.

## Gleicher Test, anderes Modell

```mermaid
flowchart LR
    T["📏 dieselben Testfälle"] --> A["anthropic<br/>Claude"]
    T --> H["adesso-hub<br/>DeepSeek · Qwen"]
    A --> C["📊 Vergleich:<br/>welches Modell taugt<br/>für diesen Skill?"]
    H --> C
```

## Kernaussage

> **Jede Skill-Änderung bekommt einen kurzen Prüflauf.** So bleibt ein Skill verlässlich, auch wenn er wächst oder das Modell wechselt.
