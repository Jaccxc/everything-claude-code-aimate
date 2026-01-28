#!/usr/bin/env python3
"""
PreCompact Hook - Save state before context compaction.

Cross-platform (Windows, macOS, Linux)

Runs before Claude compacts context, giving you a chance to
preserve important state that might get lost in summarization.
"""

import sys
from datetime import datetime
from pathlib import Path


def get_claude_dir() -> Path:
    """Get the Claude config directory."""
    return Path.home() / ".claude"


def get_sessions_dir() -> Path:
    """Get the sessions directory."""
    return get_claude_dir() / "sessions"


def main():
    sessions_dir = get_sessions_dir()
    compaction_log = sessions_dir / "compaction-log.txt"
    
    sessions_dir.mkdir(parents=True, exist_ok=True)
    
    # Log compaction event with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(compaction_log, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Context compaction triggered\n")
    
    # If there's an active session file, note the compaction
    sessions = sorted(
        sessions_dir.glob("*-session.tmp"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    if sessions:
        active_session = sessions[0]
        time_str = datetime.now().strftime("%H:%M")
        with open(active_session, "a", encoding="utf-8") as f:
            f.write(f"\n---\n**[Compaction occurred at {time_str}]** - Context was summarized\n")
    
    print("[PreCompact] State saved before compaction", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[PreCompact] Error: {e}", file=sys.stderr)
