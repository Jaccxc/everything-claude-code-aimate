#!/usr/bin/env python3
"""
SessionEnd Hook - Evaluate session for extractable patterns.

Cross-platform (Windows, macOS, Linux)

Runs at the end of each session to evaluate if any patterns
should be extracted as learned skills.
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


def get_learned_skills_dir() -> Path:
    """Get the learned skills directory."""
    return get_claude_dir() / "skills" / "learned"


def main():
    """
    Evaluate the session for patterns that could become learned skills.
    
    This is a placeholder that logs evaluation metrics. The actual
    pattern extraction requires analyzing the session transcript,
    which should be done by the continuous-learning skill/agent.
    """
    sessions_dir = get_sessions_dir()
    learned_dir = get_learned_skills_dir()
    
    learned_dir.mkdir(parents=True, exist_ok=True)
    
    # Log that evaluation was triggered
    evaluation_log = sessions_dir / "evaluation-log.txt"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(evaluation_log, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Session evaluation triggered\n")
    
    # Count existing learned skills
    learned_count = len(list(learned_dir.glob("*.md")))
    
    print(f"[EvaluateSession] Session evaluated - {learned_count} learned skills in library", file=sys.stderr)
    print("[EvaluateSession] Use /learn command to manually extract patterns", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[EvaluateSession] Error: {e}", file=sys.stderr)
