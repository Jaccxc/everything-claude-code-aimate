#!/usr/bin/env python3
"""
Continuous Learning v2 - Observation Hook

Captures tool use events for pattern analysis.
Claude Code passes hook data via stdin as JSON.

Cross-platform: Works on Windows, macOS, and Linux.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def get_config_dir() -> Path:
    """Get the homunculus config directory."""
    return Path.home() / ".claude" / "homunculus"


def get_observations_file() -> Path:
    """Get the observations file path."""
    return get_config_dir() / "observations.jsonl"


def archive_if_needed(observations_file: Path, max_size_mb: int = 10):
    """Archive observations file if it exceeds max size."""
    if not observations_file.exists():
        return
    
    try:
        size_mb = observations_file.stat().st_size / (1024 * 1024)
        if size_mb >= max_size_mb:
            archive_dir = get_config_dir() / "observations.archive"
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            archive_path = archive_dir / f"observations-{timestamp}.jsonl"
            observations_file.rename(archive_path)
    except OSError:
        pass


def parse_hook_input(input_json: str) -> dict:
    """Parse the hook input JSON."""
    try:
        data = json.loads(input_json)
        
        # Extract fields - Claude Code hook format
        hook_type = data.get("hook_type", "unknown")
        tool_name = data.get("tool_name", data.get("tool", "unknown"))
        tool_input = data.get("tool_input", data.get("input", {}))
        tool_output = data.get("tool_output", data.get("output", ""))
        session_id = data.get("session_id", "unknown")
        
        # Truncate large inputs/outputs
        if isinstance(tool_input, dict):
            tool_input_str = json.dumps(tool_input)[:5000]
        else:
            tool_input_str = str(tool_input)[:5000]
        
        if isinstance(tool_output, dict):
            tool_output_str = json.dumps(tool_output)[:5000]
        else:
            tool_output_str = str(tool_output)[:5000]
        
        # Determine event type
        event = "tool_start" if "Pre" in hook_type else "tool_complete"
        
        return {
            "parsed": True,
            "event": event,
            "tool": tool_name,
            "input": tool_input_str if event == "tool_start" else None,
            "output": tool_output_str if event == "tool_complete" else None,
            "session": session_id,
        }
    except Exception as e:
        return {"parsed": False, "error": str(e)}


def write_observation(observation: dict, observations_file: Path):
    """Write observation to file."""
    observations_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(observations_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(observation) + "\n")


def main():
    config_dir = get_config_dir()
    observations_file = get_observations_file()
    
    # Ensure directory exists
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Skip if disabled
    if (config_dir / "disabled").exists():
        sys.exit(0)
    
    # Read JSON from stdin
    try:
        input_json = sys.stdin.read()
    except Exception:
        sys.exit(0)
    
    if not input_json.strip():
        sys.exit(0)
    
    # Parse input
    parsed = parse_hook_input(input_json)
    
    # Get current timestamp
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    if not parsed.get("parsed"):
        # Log parse error for debugging
        observation = {
            "timestamp": timestamp,
            "event": "parse_error",
            "raw": input_json[:1000],
        }
        write_observation(observation, observations_file)
        sys.exit(0)
    
    # Archive if file too large
    archive_if_needed(observations_file)
    
    # Build observation
    observation = {
        "timestamp": timestamp,
        "event": parsed["event"],
        "tool": parsed["tool"],
        "session": parsed["session"],
    }
    
    if parsed.get("input"):
        observation["input"] = parsed["input"]
    if parsed.get("output"):
        observation["output"] = parsed["output"]
    
    # Write observation
    write_observation(observation, observations_file)


if __name__ == "__main__":
    main()
