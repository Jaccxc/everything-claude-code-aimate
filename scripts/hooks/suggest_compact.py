#!/usr/bin/env python3
"""
Strategic Compact Suggester.

Cross-platform (Windows, macOS, Linux)

Runs on PreToolUse or periodically to suggest manual compaction at logical intervals.

Why manual over auto-compact:
- Auto-compact happens at arbitrary points, often mid-task
- Strategic compacting preserves context through logical phases
- Compact after exploration, before execution
- Compact after completing a milestone, before starting next
"""

import os
import sys
import tempfile
from pathlib import Path


def main():
    # Track tool call count (increment in a temp file)
    session_id = os.environ.get("CLAUDE_SESSION_ID") or os.environ.get("PPID") or "default"
    counter_file = Path(tempfile.gettempdir()) / f"claude-tool-count-{session_id}"
    threshold = int(os.environ.get("COMPACT_THRESHOLD", "50"))
    
    count = 1
    
    # Read existing count or start at 1
    if counter_file.exists():
        try:
            count = int(counter_file.read_text().strip()) + 1
        except (ValueError, OSError):
            count = 1
    
    # Save updated count
    counter_file.write_text(str(count))
    
    # Suggest compact after threshold tool calls
    if count == threshold:
        print(f"[StrategicCompact] {threshold} tool calls reached - consider /compact if transitioning phases", file=sys.stderr)
    
    # Suggest at regular intervals after threshold
    if count > threshold and count % 25 == 0:
        print(f"[StrategicCompact] {count} tool calls - good checkpoint for /compact if context is stale", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[StrategicCompact] Error: {e}", file=sys.stderr)
