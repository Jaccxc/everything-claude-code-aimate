#!/usr/bin/env python3
"""
Stop Hook: Check for print() statements in modified Python files.

This hook runs after each response and checks if any modified
Python files contain print() statements that might be debug code.
It provides warnings to help developers remember to remove
debug statements before committing.

Replaces check-console-log.js for Python projects.
"""

import subprocess
import sys
from pathlib import Path


def main():
    # Read stdin (hook data)
    data = sys.stdin.read()
    
    try:
        # Check if we're in a git repository
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            # Not in a git repo, just pass through the data
            print(data)
            return
        
        # Get list of modified files
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True,
            text=True
        )
        
        files = [
            f for f in result.stdout.strip().split("\n")
            if f.endswith(".py") and Path(f).exists()
        ]
        
        has_print = False
        
        # Check each file for print() statements
        for file in files:
            content = Path(file).read_text(encoding="utf-8")
            # Simple check - look for print( that's not in a comment or string
            # This is a basic heuristic
            lines = content.split("\n")
            for line_num, line in enumerate(lines, 1):
                stripped = line.lstrip()
                if stripped.startswith("#"):
                    continue
                if "print(" in line and not '"""' in line and not "'''" in line:
                    print(f"[Hook] WARNING: print() found in {file}:{line_num}", file=sys.stderr)
                    has_print = True
        
        if has_print:
            print("[Hook] Consider removing print() statements or using logger before committing", file=sys.stderr)
    
    except Exception:
        # Silently ignore errors (git might not be available, etc.)
        pass
    
    # Always output the original data
    print(data)


if __name__ == "__main__":
    main()
