#!/usr/bin/env python3
"""
SessionStart Hook - Load previous context on new session.

Cross-platform (Windows, macOS, Linux)

Runs when a new Claude session starts. Checks for recent session
files and notifies Claude of available context to load.
"""

import sys
from datetime import datetime, timedelta
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


def find_recent_files(directory: Path, pattern: str, max_age_days: int = 7) -> list[Path]:
    """Find files matching pattern modified within max_age_days."""
    if not directory.exists():
        return []
    
    cutoff = datetime.now().timestamp() - (max_age_days * 24 * 60 * 60)
    files = []
    
    for f in directory.glob(pattern):
        if f.is_file() and f.stat().st_mtime >= cutoff:
            files.append(f)
    
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)


def is_poetry_project(project_dir: Path = None) -> bool:
    """Check if the directory is a Poetry project."""
    project_dir = project_dir or Path.cwd()
    return (project_dir / "pyproject.toml").exists()


def main():
    sessions_dir = get_sessions_dir()
    learned_dir = get_learned_skills_dir()
    
    # Ensure directories exist
    sessions_dir.mkdir(parents=True, exist_ok=True)
    learned_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for recent session files (last 7 days)
    recent_sessions = find_recent_files(sessions_dir, "*-session.tmp", max_age_days=7)
    
    if recent_sessions:
        latest = recent_sessions[0]
        print(f"[SessionStart] Found {len(recent_sessions)} recent session(s)", file=sys.stderr)
        print(f"[SessionStart] Latest: {latest}", file=sys.stderr)
    
    # Check for learned skills
    learned_skills = list(learned_dir.glob("*.md"))
    
    if learned_skills:
        print(f"[SessionStart] {len(learned_skills)} learned skill(s) available in {learned_dir}", file=sys.stderr)
    
    # Detect project type
    cwd = Path.cwd()
    if is_poetry_project(cwd):
        print("[SessionStart] Poetry project detected", file=sys.stderr)
        if (cwd / "poetry.lock").exists():
            print("[SessionStart] poetry.lock found - dependencies are locked", file=sys.stderr)
    elif (cwd / "requirements.txt").exists():
        print("[SessionStart] requirements.txt found - pip project detected", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[SessionStart] Error: {e}", file=sys.stderr)
