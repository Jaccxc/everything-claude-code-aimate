#!/usr/bin/env python3
"""
Continuous Learning - Session Evaluator

Runs on Stop hook to extract reusable patterns from Claude Code sessions.

Why Stop hook instead of UserPromptSubmit:
- Stop runs once at session end (lightweight)
- UserPromptSubmit runs every message (heavy, adds latency)

Cross-platform: Works on Windows, macOS, and Linux.
"""

import json
import os
import sys
from pathlib import Path


def get_config_dir() -> Path:
    """Get the script's directory."""
    return Path(__file__).parent


def get_learned_skills_path() -> Path:
    """Get the path for learned skills."""
    return Path.home() / ".claude" / "skills" / "learned"


def load_config() -> dict:
    """Load configuration from config.json."""
    config_file = get_config_dir() / "config.json"
    if config_file.exists():
        try:
            return json.loads(config_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def count_messages(transcript_path: Path) -> int:
    """Count user messages in transcript."""
    if not transcript_path.exists():
        return 0
    
    try:
        content = transcript_path.read_text(encoding="utf-8")
        # Simple count of user message indicators
        return content.count('"type":"user"') + content.count('"type": "user"')
    except (OSError, UnicodeDecodeError):
        return 0


def main():
    config = load_config()
    min_session_length = config.get("min_session_length", 10)
    
    # Get learned skills path
    learned_path_str = config.get("learned_skills_path", "")
    if learned_path_str:
        learned_skills_path = Path(learned_path_str.replace("~", str(Path.home())))
    else:
        learned_skills_path = get_learned_skills_path()
    
    # Ensure directory exists
    learned_skills_path.mkdir(parents=True, exist_ok=True)
    
    # Get transcript path from environment
    transcript_path_str = os.environ.get("CLAUDE_TRANSCRIPT_PATH", "")
    
    if not transcript_path_str:
        sys.exit(0)
    
    transcript_path = Path(transcript_path_str)
    if not transcript_path.exists():
        sys.exit(0)
    
    # Count messages
    message_count = count_messages(transcript_path)
    
    # Skip short sessions
    if message_count < min_session_length:
        print(
            f"[ContinuousLearning] Session too short ({message_count} messages), skipping",
            file=sys.stderr
        )
        sys.exit(0)
    
    # Signal to Claude that session should be evaluated
    print(
        f"[ContinuousLearning] Session has {message_count} messages - evaluate for extractable patterns",
        file=sys.stderr
    )
    print(
        f"[ContinuousLearning] Save learned skills to: {learned_skills_path}",
        file=sys.stderr
    )


if __name__ == "__main__":
    main()
