# Refactor Clean

Remove dead code and unused dependencies safely:

1. **Run analysis:**
   ```bash
   # Check for unused imports
   poetry run ruff check . --select=F401
   
   # Find unused variables
   poetry run ruff check . --select=F841
   
   # Check for unreachable code
   poetry run ruff check . --select=F811,F821
   ```

2. **Identify dead code patterns:**
   - Functions with zero calls (search with grep)
   - Unused class methods
   - Commented-out code blocks
   - Variables assigned but never read
   - Unreachable code after return/raise

3. **For each candidate:**
   - Verify it's truly unused (search entire codebase)
   - Check it's not called dynamically (getattr, etc.)
   - Check it's not exported via `__all__`
   - Confirm no tests depend on it

4. **Clean in order:**
   - Unused imports first
   - Unused variables
   - Unused functions (bottom-up)
   - Unused classes (after their methods)
   - Empty files

5. **Verify after each removal:**
   ```bash
   poetry run ruff check .
   poetry run pytest
   ```

6. **Clean dependencies:**
   ```bash
   # List all dependencies
   poetry show
   
   # Check for unused imports in pyproject.toml
   # Remove if no import found in codebase
   ```

7. **Track changes:**
   - Log what was removed
   - Commit in small chunks
   - Easy rollback if needed

## Safety Rules

- Never remove anything with external references
- Keep test utilities even if only used in tests
- Preserve public API exports
- Keep backwards compatibility shims with comments
- When uncertain, comment out first, remove later

## Common Patterns to Clean

```python
# ❌ REMOVE: Unused import
from typing import Optional  # Not used, and should use str | None anyway

# ❌ REMOVE: Assigned but never read
temp = calculate_value()  # F841: local variable 'temp' assigned but never used

# ❌ REMOVE: Unreachable code
def example():
    return "done"
    print("never runs")  # Unreachable

# ⚠️ CHECK: Might be used dynamically
def _internal_helper():
    pass  # Check for getattr() calls before removing
```

Clean code is maintainable code!
