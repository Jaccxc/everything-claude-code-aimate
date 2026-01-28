# Hooks

Hooks trigger automation at specific events. See `/hooks/hooks.json` for the full configuration.

## Available Hooks

### PreToolUse
Runs before a tool executes. Can block or modify behavior.

- **Documentation blocker**: Prevents creating random .md files outside of standard locations
- **git push reminder**: Reminds to review changes before pushing

### PostToolUse
Runs after a tool completes. Good for formatting and validation.

- **Auto-format Python**: Runs `poetry run ruff format` and `poetry run black` after editing Python files
- **Ruff lint check**: Checks for lint errors after Python edits
- **print() warning**: Warns about debug print statements

### Stop
Runs when Claude stops responding.

- **print() checker**: Scans modified Python files for print() statements

### SessionStart
Runs when a new session begins.

- **Context loader**: Loads previous session state if available

### SessionEnd
Runs when session ends.

- **State persister**: Saves session state for next time

### PreCompact
Runs before context compaction.

- **State saver**: Preserves important state before compaction

## Creating New Hooks

Add to `hooks/hooks.json`:

```json
{
  "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\\\.py$\"",
  "hooks": [{
    "type": "command",
    "command": "python -c \"import sys; ...\""
  }],
  "description": "What this hook does"
}
```

## Matcher Syntax

- `tool == "Bash"` - Match specific tool
- `tool_input.file_path matches "\\.py$"` - Regex on input
- `tool_input.command matches "(poetry|pytest)"` - Command patterns
- `*` - Match everything (use sparingly)

## Best Practices

1. **Keep hooks fast** - Long hooks slow down Claude
2. **Fail gracefully** - Don't block on non-critical errors
3. **Use stderr for messages** - stdout goes back to Claude
4. **Test thoroughly** - Broken hooks can disrupt workflow
