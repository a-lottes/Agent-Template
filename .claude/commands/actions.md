---
description: Show open actions, decisions and risks from the project memory (memory/)
argument-hint: "[optional filter, e.g. owner or topic]"
---

Project memory:

!`for f in memory/actions.md memory/decisions.md memory/risks.md; do [ -f "$f" ] && { echo "=== $f"; cat "$f"; echo; }; done; [ -d memory ] || echo "memory/ is empty: nothing processed yet."`

Filter (optional): $ARGUMENTS

From the project memory above, list all open actions as a table: Action | Owner | Due | Status.
Mark items without an owner and items past their due date (today's date is in your context).
Then add the decisions and risks as short bullet lists. Apply the filter if one was given.
Answer in the user's language. Do nothing else.
