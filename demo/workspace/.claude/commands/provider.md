---
description: Show or switch the model provider of this workspace (anthropic | adesso-hub | adesso-hub-claude)
argument-hint: "[anthropic | adesso-hub | adesso-hub-claude]"
allowed-tools: Bash(./project-memory/scripts/provider.sh:*)
---

Provider switch result:

!`./project-memory/scripts/provider.sh $ARGUMENTS`

Repeat the provider and the three model mappings above as a short table. If a profile was written,
end with exactly one line: "Neu starten: `/exit`, dann `claude -c` (Gespräch läuft weiter)."
Do nothing else.
