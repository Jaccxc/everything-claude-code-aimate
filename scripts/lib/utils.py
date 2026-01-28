"""
Cross-platform utility functions for Claude Code hooks and scripts.
Works on Windows, macOS, and Linux.

Python version - replaces the original JavaScript implementation.
"""

import json
import os
import re
import sys
import subprocess
from datetime import datetime
from pathlib import Path


# Platform detection
IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")


def get_home_dir() -> Path:
    """Get the user's home directory (cross-platform)."""
    return Path.home()


def get_claude_dir() -> Path:
    """Get the Claude config directory."""
    return get_home_dir() / ".claude"


def get_sessions_dir() -> Path:
    """Get the sessions directory."""
    return get_claude_dir() / "sessions"


def get_learned_skills_dir() -> Path:
    """Get the learned skills directory."""
    return get_claude_dir() / "skills" / "learned"


def get_temp_dir() -> Path:
    """Get the temp directory (cross-platform)."""
    import tempfile
    return Path(tempfile.gettempdir())


def ensure_dir(dir_path: Path | str) -> Path:
    """Ensure a directory exists (create if not)."""
    path = Path(dir_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_date_string() -> str:
    """Get current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


def get_time_string() -> str:
    """Get current time in HH:MM format."""
    return datetime.now().strftime("%H:%M")


def get_datetime_string() -> str:
    """Get current datetime in YYYY-MM-DD HH:MM:SS format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_session_id_short(fallback: str = "default") -> str:
    """
    Get short session ID from CLAUDE_SESSION_ID environment variable.
    Returns the last 8 characters for uniqueness with brevity.
    """
    session_id = os.environ.get("CLAUDE_SESSION_ID", "")
    if not session_id:
        return fallback
    return session_id[-8:]


def find_files(
    directory: Path | str,
    pattern: str,
    max_age_days: float | None = None,
    recursive: bool = False
) -> list[dict]:
    """
    Find files matching a pattern in a directory.
    
    Args:
        directory: Directory to search
        pattern: File pattern (e.g., "*.tmp", "*.md")
        max_age_days: Only include files modified within this many days
        recursive: Search subdirectories
    
    Returns:
        List of dicts with 'path' and 'mtime' keys, sorted by mtime (newest first)
    """
    directory = Path(directory)
    if not directory.exists():
        return []
    
    # Convert glob pattern to regex
    regex_pattern = pattern.replace(".", r"\.").replace("*", ".*").replace("?", ".")
    regex = re.compile(f"^{regex_pattern}$")
    
    results = []
    
    def search_dir(current_dir: Path):
        try:
            for entry in current_dir.iterdir():
                if entry.is_file() and regex.match(entry.name):
                    stat = entry.stat()
                    if max_age_days is not None:
                        age_days = (datetime.now().timestamp() - stat.st_mtime) / (60 * 60 * 24)
                        if age_days > max_age_days:
                            continue
                    results.append({"path": str(entry), "mtime": stat.st_mtime})
                elif entry.is_dir() and recursive:
                    search_dir(entry)
        except PermissionError:
            pass
    
    search_dir(directory)
    results.sort(key=lambda x: x["mtime"], reverse=True)
    return results


def read_stdin_json() -> dict:
    """Read JSON from stdin (for hook input)."""
    try:
        data = sys.stdin.read()
        if data.strip():
            return json.loads(data)
        return {}
    except json.JSONDecodeError:
        return {}


def log(message: str) -> None:
    """Log to stderr (visible to user in Claude Code)."""
    print(message, file=sys.stderr)


def output(data) -> None:
    """Output to stdout (returned to Claude)."""
    if isinstance(data, (dict, list)):
        print(json.dumps(data))
    else:
        print(data)


def read_file(file_path: Path | str) -> str | None:
    """Read a text file safely."""
    try:
        return Path(file_path).read_text(encoding="utf-8")
    except (OSError, IOError):
        return None


def write_file(file_path: Path | str, content: str) -> None:
    """Write a text file."""
    path = Path(file_path)
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def append_file(file_path: Path | str, content: str) -> None:
    """Append to a text file."""
    path = Path(file_path)
    ensure_dir(path.parent)
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)


def command_exists(cmd: str) -> bool:
    """Check if a command exists in PATH."""
    # Validate command name - only allow alphanumeric, dash, underscore, dot
    if not re.match(r"^[a-zA-Z0-9_.-]+$", cmd):
        return False
    
    try:
        if IS_WINDOWS:
            result = subprocess.run(
                ["where", cmd],
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                ["which", cmd],
                capture_output=True,
                text=True
            )
        return result.returncode == 0
    except Exception:
        return False


def run_command(cmd: str, cwd: str | None = None) -> dict:
    """
    Run a command and return output.
    
    SECURITY NOTE: This function executes shell commands. Only use with
    trusted, hardcoded commands. Never pass user-controlled input directly.
    
    Returns:
        dict with 'success' (bool) and 'output' (str) keys
    """
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        if result.returncode == 0:
            return {"success": True, "output": result.stdout.strip()}
        else:
            return {"success": False, "output": result.stderr or result.stdout}
    except Exception as e:
        return {"success": False, "output": str(e)}


def is_git_repo() -> bool:
    """Check if current directory is a git repository."""
    return run_command("git rev-parse --git-dir")["success"]


def get_git_modified_files(patterns: list[str] | None = None) -> list[str]:
    """Get git modified files."""
    if not is_git_repo():
        return []
    
    result = run_command("git diff --name-only HEAD")
    if not result["success"]:
        return []
    
    files = [f for f in result["output"].split("\n") if f]
    
    if patterns:
        filtered = []
        for file in files:
            for pattern in patterns:
                if re.search(pattern, file):
                    filtered.append(file)
                    break
        return filtered
    
    return files


def replace_in_file(file_path: Path | str, search: str, replace: str) -> bool:
    """Replace text in a file (cross-platform sed alternative)."""
    content = read_file(file_path)
    if content is None:
        return False
    
    new_content = content.replace(search, replace)
    write_file(file_path, new_content)
    return True


def count_in_file(file_path: Path | str, pattern: str) -> int:
    """Count occurrences of a pattern in a file."""
    content = read_file(file_path)
    if content is None:
        return 0
    
    matches = re.findall(pattern, content)
    return len(matches)


def grep_file(file_path: Path | str, pattern: str) -> list[dict]:
    """Search for pattern in file and return matching lines with line numbers."""
    content = read_file(file_path)
    if content is None:
        return []
    
    results = []
    for idx, line in enumerate(content.split("\n"), 1):
        if re.search(pattern, line):
            results.append({"line_number": idx, "content": line})
    
    return results


# Poetry-specific utilities
def is_poetry_project(project_dir: Path | None = None) -> bool:
    """Check if the directory is a Poetry project."""
    project_dir = project_dir or Path.cwd()
    return (project_dir / "pyproject.toml").exists()


def get_poetry_command(action: str) -> str:
    """
    Get the Poetry command for a given action.
    
    Args:
        action: One of 'install', 'test', 'lint', 'format', 'check', 'dev'
    """
    commands = {
        "install": "poetry install",
        "test": "poetry run pytest",
        "lint": "poetry run ruff check .",
        "format": "poetry run ruff format . && poetry run black .",
        "check": "poetry run ruff check . && poetry run black --check .",
        "dev": "poetry run uvicorn app.main:app --reload",
    }
    return commands.get(action, f"poetry run {action}")
