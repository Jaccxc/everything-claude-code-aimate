#!/usr/bin/env python3
"""
SessionEnd Hook - Persist session state on end.

Cross-platform (Windows, macOS, Linux)

Runs when a Claude session ends. Saves session metadata
and cleans up temporary files.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def get_claude_dir() -> Path:
    """Get the Claude config directory."""
    return Path.home() / ".claude"


def get_sessions_dir() -> Path:
    """Get the sessions directory."""
    return get_claude_dir() / "sessions"


def get_session_id_short() -> str:
    """Get short session ID from environment."""
    session_id = os.environ.get("CLAUDE_SESSION_ID", "")
    if session_id:
        return session_id[-8:]
    return "default"


def main():
    sessions_dir = get_sessions_dir()
    sessions_dir.mkdir(parents=True, exist_ok=True)
    
    session_id = get_session_id_short()
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Create session end marker
    session_file = sessions_dir / f"{date_str}-{session_id}-session.tmp"
    
    if session_file.exists():
        # Append end marker
        with open(session_file, "a", encoding="utf-8") as f:
            f.write(f"\n---\n**[Session ended at {datetime.now().strftime('%H:%M')}]**\n")
    
    # Save session metadata
    metadata_file = sessions_dir / f"{date_str}-{session_id}-metadata.json"
    metadata = {
        "session_id": session_id,
        "ended_at": datetime.now().isoformat(),
        "cwd": str(Path.cwd()),
    }
    
    metadata_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    
    print(f"[SessionEnd] Session state saved to {sessions_dir}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[SessionEnd] Error: {e}", file=sys.stderr)
