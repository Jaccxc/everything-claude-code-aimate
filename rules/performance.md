# Performance & Model Selection

## Model Selection

### Claude Opus (opus)
Use for:
- Complex architectural decisions
- Security-sensitive code review
- Large-scale refactoring
- Debugging intricate issues

### Claude Sonnet (default)
Use for:
- Standard development tasks
- Code review
- Documentation
- Most everyday work

### Claude Haiku (haiku)
Use for:
- Simple code formatting
- Repetitive tasks
- Quick lookups
- Status checks

## Context Window Management

### Keep Context Clean
- Don't read large files unnecessarily
- Use targeted file reads with line ranges
- Clear temporary context with `/compact`
- Use semantic search before full file reads

### Manage MCP Tools
- **Important:** Don't enable all MCPs at once
- 200k context can shrink to 70k with too many tools
- Keep active tools under 80
- Enable MCPs per-project basis

### File Reading Strategy
1. Start with file structure (ls, glob)
2. Use semantic search for relevant sections
3. Read specific line ranges
4. Avoid reading entire large files

## Code Quality Checks

Run checks efficiently:

```bash
# Lint check (fast)
poetry run ruff check .

# Format check (fast)
poetry run black --check .

# Run tests (slower)
poetry run pytest

# Run tests with coverage (slowest)
poetry run pytest --cov=app --cov-report=term-missing
```

## Database Performance

### Query Optimization
- Select only needed columns
- Use proper indexes
- Avoid N+1 queries with eager loading
- Use pagination for large result sets

### Connection Management
- Configure pool_size appropriately
- Set max_overflow for burst traffic
- Use connection timeout settings

## Async Performance

### Parallel Execution
```python
# ✅ GOOD: Parallel when possible
import asyncio

users, orders, stats = await asyncio.gather(
    fetch_users(),
    fetch_orders(),
    fetch_stats()
)

# ❌ BAD: Sequential when unnecessary
users = await fetch_users()
orders = await fetch_orders()
stats = await fetch_stats()
```

### Avoid Blocking
- Don't use sync operations in async context
- Use asyncpg for database operations
- Use httpx for HTTP calls
- Use aiofiles for file operations

## Memory Management

- Stream large responses
- Use generators for large data sets
- Implement pagination
- Clean up temporary files
- Close connections properly
