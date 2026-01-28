---
name: continuous-learning-v2
description: Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring, and evolves them into skills/commands/agents.
version: 2.0.0
---

# Continuous Learning v2 - Instinct-Based Architecture

An advanced learning system that turns your Claude Code sessions into reusable knowledge through atomic "instincts" - small learned behaviors with confidence scoring.

## What's New in v2

| Feature | v1 | v2 |
|---------|----|----|
| Observation | Stop hook (session end) | PreToolUse/PostToolUse (100% reliable) |
| Analysis | Main context | Background agent |
| Granularity | Full skills | Atomic "instincts" |
| Confidence | None | 0.3-0.9 weighted |
| Evolution | Direct to skill | Instincts → cluster → skill/command/agent |
| Platform | Bash only | Cross-platform Python |

## The Instinct Model

An instinct is a small learned behavior:

```yaml
---
id: prefer-pydantic-models
trigger: "when defining data structures"
confidence: 0.8
domain: "code-style"
source: "session-observation"
---

# Prefer Pydantic Models

## Action
Use Pydantic BaseModel for all data structures instead of plain dicts.

## Evidence
- Observed 5 instances of Pydantic preference
- User corrected dict-based approach to Pydantic on 2025-01-15
```

## Quick Start

### 1. Enable Observation Hooks

Add to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "python ~/.claude/skills/continuous-learning-v2/hooks/observe.py"
      }]
    }],
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "python ~/.claude/skills/continuous-learning-v2/hooks/observe.py"
      }]
    }]
  }
}
```

### 2. Initialize Directory Structure

```bash
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path "$HOME\.claude\homunculus\instincts\personal"
New-Item -ItemType Directory -Force -Path "$HOME\.claude\homunculus\instincts\inherited"
New-Item -ItemType Directory -Force -Path "$HOME\.claude\homunculus\evolved\agents"
New-Item -ItemType Directory -Force -Path "$HOME\.claude\homunculus\evolved\skills"
New-Item -ItemType Directory -Force -Path "$HOME\.claude\homunculus\evolved\commands"
New-Item -ItemType File -Force -Path "$HOME\.claude\homunculus\observations.jsonl"

# macOS/Linux
mkdir -p ~/.claude/homunculus/{instincts/{personal,inherited},evolved/{agents,skills,commands}}
touch ~/.claude/homunculus/observations.jsonl
```

## Commands

| Command | Description |
|---------|-------------|
| `/instinct-status` | Show all learned instincts with confidence |
| `/evolve` | Cluster related instincts into skills/commands |
| `/instinct-export` | Export instincts for sharing |
| `/instinct-import <file>` | Import instincts from others |

## Configuration

Edit `config.json`:

```json
{
  "version": "2.0",
  "observation": {
    "enabled": true,
    "store_path": "~/.claude/homunculus/observations.jsonl",
    "max_file_size_mb": 10,
    "archive_after_days": 7
  },
  "instincts": {
    "personal_path": "~/.claude/homunculus/instincts/personal/",
    "inherited_path": "~/.claude/homunculus/instincts/inherited/",
    "min_confidence": 0.3,
    "auto_approve_threshold": 0.7,
    "confidence_decay_rate": 0.05
  },
  "evolution": {
    "cluster_threshold": 3,
    "evolved_path": "~/.claude/homunculus/evolved/"
  }
}
```

## Cross-Platform Support

All scripts are Python-based and work on:
- Windows (PowerShell, cmd)
- macOS (zsh, bash)
- Linux (bash, zsh)

Requirements:
- Python 3.9+
- No additional dependencies (stdlib only)

## File Structure

```
~/.claude/homunculus/
├── observations.jsonl      # Current session observations
├── observations.archive/   # Processed observations
├── instincts/
│   ├── personal/           # Auto-learned instincts
│   └── inherited/          # Imported from others
└── evolved/
    ├── agents/             # Generated specialist agents
    ├── skills/             # Generated skills
    └── commands/           # Generated commands
```

## Confidence Scoring

| Score | Meaning | Behavior |
|-------|---------|----------|
| 0.3 | Tentative | Suggested but not enforced |
| 0.5 | Moderate | Applied when relevant |
| 0.7 | Strong | Auto-approved for application |
| 0.9 | Near-certain | Core behavior |

**Confidence increases** when:
- Pattern is repeatedly observed
- User doesn't correct the suggested behavior
- Similar instincts from other sources agree

**Confidence decreases** when:
- User explicitly corrects the behavior
- Pattern isn't observed for extended periods
- Contradicting evidence appears

## Privacy

- Observations stay **local** on your machine
- Only **instincts** (patterns) can be exported
- No actual code or conversation content is shared
- You control what gets exported

---

*Instinct-based learning: teaching Claude your patterns, one observation at a time.*
