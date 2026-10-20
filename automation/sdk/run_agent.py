"""Run the Project Memory agent from Python via the Claude Agent SDK.

pip install claude-agent-sdk
Check option names against the current SDK docs before the demo.
"""
import asyncio
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, query

PROJECT = Path.home() / "agent-demo"


async def main() -> None:
    options = ClaudeAgentOptions(
        cwd=str(PROJECT),
        plugins=[{"type": "local", "path": str(PROJECT / "project-memory")}],
        setting_sources=["project"],      # loads .claude/settings.json (AI Hub) and CLAUDE.md
        permission_mode="acceptEdits",
    )
    async for message in query(prompt="/project-memory:process-inbox", options=options):
        print(message)


if __name__ == "__main__":
    asyncio.run(main())
