# 02 · Wie ein Skill arbeitet (visuell)

## Ein Skill ist eine Anleitung mit Schnittstelle

```mermaid
flowchart TB
    subgraph SKILL["📁 skills/meeting-to-actions"]
        direction TB
        FM["🏷️ Frontmatter<br/><b>name</b> + <b>description</b><br/><i>immer geladen · wenige Tokens</i>"]
        BODY["📋 Anleitung<br/>Schritte · Regeln<br/><i>nur bei Bedarf geladen</i>"]
        TPL["📐 Ausgabeformat<br/>Tabellen für actions · decisions · risks<br/><i>Teil der Anleitung</i>"]
        FM --> BODY --> TPL
    end

    style FM fill:#2da44e,color:#fff
    style BODY fill:#8957e5,color:#fff
    style TPL fill:#6e7781,color:#fff
```

> **Progressive Disclosure:** Claude kennt von jedem Skill nur das Etikett. Den Inhalt liest er erst, wenn das Etikett zur Aufgabe passt. So kann man viele Skills haben, ohne den Kontext zu verstopfen.

## Wann löst ein Skill aus?

```mermaid
flowchart LR
    P(["💬 Bitte des Nutzers"]) --> M{"Passt sie zur<br/>Beschreibung<br/>eines Skills?"}
    M -->|"ja: „Protokoll in inbox/,<br/>Projektgedächtnis aktualisieren“"| L["📋 Skill-Inhalt laden"]
    M -->|"nein: „Was ist eine<br/>RACI-Matrix?“"| N["💡 normale Antwort<br/>ohne Skill"]
    L --> W["🤖 nach Anleitung arbeiten"]
    S(["⌨️ /project-memory:process-inbox"]) -->|"explizit, immer"| L
```

## Was der Skill im Projekt anstößt

```mermaid
sequenceDiagram
    autonumber
    actor Nutzer
    participant Main as Claude (Hauptsession)
    participant T as doc-triage · haiku
    participant E as action-extractor · sonnet
    participant R as reviewer · opus
    participant Mem as memory/

    Nutzer->>Main: „Projektgedächtnis aktualisieren“
    Main->>Main: Skill meeting-to-actions laden
    Main->>T: Was ist neu in inbox/?
    T-->>Main: 1 neues Protokoll
    Main->>E: Entscheidungen, Aufgaben, Risiken extrahieren
    E-->>Main: Befunde mit Zitat
    Main->>R: Jeden Befund gegen die Quelle prüfen
    R-->>Main: verified / unsupported
    Main->>Mem: nur geprüfte Befunde schreiben
    Main-->>Nutzer: Zusammenfassung + Abgelehntes
```

## Wo ein Skill liegt, bestimmt, wer ihn hat

```mermaid
flowchart LR
    A["👤 ~/.claude/skills/<br/>nur ich"] --> B["📁 .claude/skills/<br/>alle im Projekt"] --> C["📦 Plugin + Marktplatz<br/>ganzes Team, versioniert"]
    style A fill:#ddf4ff
    style B fill:#b6e3ff
    style C fill:#54aeff,color:#fff
```

## Acht Regeln auf einen Blick

```mermaid
mindmap
  root((Skill<br/>richtig<br/>einsetzen))
    Schnittstelle
      Eine Aufgabe pro Skill
      Beschreibung sagt WANN
      Echte Auslöser-Wörter
    Inhalt
      Nummerierte Schritte
      Harte Regeln
      Format per Template
    Robustheit
      Deterministisches in Skripte
      Abhängigkeiten eindeutig benennen
    Betrieb
      Ablageort nach Reichweite
      Vor dem Verteilen validieren
```

## Kernaussage

> **Die Beschreibung ist die Schnittstelle, die Anleitung die Implementierung.** Weil der Skill nur eine Anleitung ist, lässt er sich mit ein paar Zeilen erweitern. Das machen wir als Nächstes.
