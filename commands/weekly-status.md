---
description: Draft a weekly status report from the project memory (Markdown and PDF).
---

Read `memory/decisions.md`, `memory/actions.md` and `memory/risks.md`. Draft `memory/status-draft.md` with: highlights, decisions this week, open actions grouped by owner (overdue first), top three risks, and questions for the steering committee. Use only facts from the memory files.

After writing the draft, save it as a PDF next to the Markdown (the PDF is stored beside the Markdown file):

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/meeting-to-actions/scripts/md_to_pdf.py memory/status-draft.md
```
